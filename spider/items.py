from scrapy import Item, Field


class Meme(Item):
    title = Field()
    youtube_id = Field()
    keywords = Field()
    types = Field()
    origin = Field()
    status = Field()
    year = Field()
    image = Field()
    other = Field()
