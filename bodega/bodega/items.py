# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy




class BodegaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field(serializer=str)
    Wholesale_Price = scrapy.Field(serializer=str)
    Price = scrapy.Field(serializer=str)
    SKU  = scrapy.Field(serializer=str)
    Model_number = scrapy.Field(serializer=str)
    link = scrapy.Field(serializer=str)
    SB  = scrapy.Field(serializer=str)


 
