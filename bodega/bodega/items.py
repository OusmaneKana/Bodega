# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy




class BodegaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=str)
    link = scrapy.Field(serializer=str)

 
