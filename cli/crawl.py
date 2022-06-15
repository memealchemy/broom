from scrapy import cmdline
import click


@click.command()
def crawl():
    """Crawl memes using the scrapy spider"""
    cmdline.execute("scrapy crawl memes -o ../../output.json".split())
