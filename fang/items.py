# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    sale = scrapy.Field()
    origin_url = scrapy.Field()

class ESFHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    origin_url = scrapy.Field()
