from urllib.parse import quote_plus, unquote_plus
import random
import time
import json
import re

import scrapy
import scrapetube
from fuzzywuzzy import process
from scrapy.http import HtmlResponse

from spider.items import Meme
from .helpers import Utils, Invalids


class MemeSpider(scrapy.Spider):
    name = "memes"
    allowed_domains = ["youtube.com", "google.com", "html.duckduckgo.com"]
    videos = list(
        scrapetube.get_channel("UCaHT88aobpcvRFEuy4v5Clg", limit=200, sleep=0.2)
    )
    start_urls = [
        "https://youtube.com/oembed?url=https://youtube.com/watch?v=" + v["videoId"]
        for v in videos
    ]

    def parse(self, response: HtmlResponse):
        string = (
            json.loads(response.text)["title"].replace("“", '"').replace("”", '"')
        )  # type: str

        title = Utils.regex.sub("", string).strip()
        words = re.findall('"([^"]*)"', string)
        meme = None

        if len(words) > 0:
            meme = quote_plus(
                "".join([s.split("_")[0] for s in words[0]]).strip().lower()
            ).strip()
        else:
            meme = quote_plus(Utils.tokenize(title).lower()).strip()

        yield scrapy.Request(
            f"https://knowyourmeme.com/search?context=entries&sort=relevance&q={meme}+category_name%3Ameme",
            callback=self.parse_kym_url,
            headers={"User-Agent": "Mozilla/5.0"},
            dont_filter=True,
            meta={"meme": meme, "youtube_id": response.url.split("?v=")[1]},
        )

    def parse_kym_url(self, response: HtmlResponse):
        meme = unquote_plus(response.meta["meme"].replace("+", " ").strip().title())
        results = response.xpath(
            '//tbody[@class="entry-grid-body infinite"]//a/text()'
        ).getall()

        while "\n" in results:
            results.remove("\n")

        matches = process.extract(meme, results, limit=len(results))

        try:
            url = (
                "https://knowyourmeme.com/memes/"
                + max(matches, key=lambda x: x[-1])[0]
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "-")
                .replace("/-", "")
                .replace(",", "")
                .replace("’", "")
                .replace("!", "")
                .replace("'", "")
                .lower()
            )

            yield scrapy.Request(
                url,
                callback=self.parse_kym_table,
                headers={"User-Agent": "Mozilla/5.0"},
                dont_filter=True,
                meta={
                    "meme": max(matches, key=lambda x: x[-1])[0],
                    "youtube_id": response.meta["youtube_id"],
                },
            )
        except Exception:
            yield scrapy.Request(
                f"https://google.com/search?q={meme}+know+your+meme",
                callback=self.parse_kym_google,
                headers={"User-Agent": "Mozilla/5.0"},
                dont_filter=True,
                meta={"meme": meme, "youtube_id": response.meta["youtube_id"]},
            )

    def parse_kym_google(self, response: HtmlResponse):
        try:
            url = (
                [
                    url
                    for url in response.xpath("//a/@href").getall()
                    if "knowyourmeme.com/memes" in url
                ][0]
                .split("?q=")[1]
                .split("&sa")[0]
            )

            yield scrapy.Request(
                url,
                callback=self.parse_kym_table,
                dont_filter=True,
                meta={
                    "meme": response.meta["meme"],
                    "youtube_id": response.meta["youtube_id"],
                },
                headers={"User-Agent": "Mozilla/5.0"},
            )
            time.sleep(1.7)
        except Exception:
            print(
                f'Yielding limited info as nothing was found for {response.meta["meme"]} :('
            )

            item = Meme()

            item["title"] = response.meta["meme"]
            item["youtube_id"] = response.meta["youtube_id"]
            item["types"] = "None"
            item["status"] = "None"
            item["year"] = "None"
            item["image"] = "None"
            item["other"] = "None"

            yield item

    def parse_kym_table(self, response: HtmlResponse):
        details = response.xpath('//div[@class = "details"]//text()').getall()

        while "\n" in details:
            details.remove("\n")
        details = [d.replace("\n", "") for d in details]

        try:
            if details[2] == Invalids.RESEARCH[0]:
                del details[2]
                del details[2]
        except IndexError:
            pass

        item = Meme()
        item["title"] = response.meta["meme"]
        item["youtube_id"] = response.meta["youtube_id"]

        types = "None"
        try:
            types = details[-(len(details) - details.index("Type:") - 1) :]
        except ValueError:
            pass
        item["types"] = types

        item["status"] = details[1]
        item["origin"] = details[3]
        item["year"] = details[5]

        try:
            item["image"] = random.choice(
                response.xpath(
                    '//img[@class=" kym-image image-auto-link"]/@data-src'
                ).getall()
            )
        except IndexError:
            item["image"] = Utils.QUESTION_MARK

        try:
            item["other"] = random.choice(response.xpath("//iframe/@src").getall())
        except IndexError:
            item["other"] = Utils.QUESTION_MARK

        print(item.__dict__)

        yield item
        time.sleep(1.7)