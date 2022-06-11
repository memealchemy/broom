import json

import scrapy
from scrapy.http import HtmlResponse


class RevisionSpider(scrapy.Spider):
    name = "revision"
    start_urls = (
        f"https://youtube.com/oembed?url=https://youtube.com/watch?v={v['youtube_id']}"
        for v in json.load(open("output.fix.json"))
    )

    def parse(self, response: HtmlResponse):
        pass
