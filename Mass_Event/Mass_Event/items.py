# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MassEventItem(scrapy.Item):
    # define the fields for your item here like:
    event_name = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    location = scrapy.Field()
    interested_going = scrapy.Field()
    # going = scrapy.Field()
