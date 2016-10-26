# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnaptItem(scrapy.Item):
      product_name = scrapy.Field()
      price= scrapy.Field()
      url = scrapy.Field()
      image= scrapy.Field()
      excerpts= scrapy.Field()

class SnapdealItem(scrapy.Item):
      product_name = scrapy.Field()
      desc= scrapy.Field()
      specs=scrapy.Field()
      url = scrapy.Field()
      price= scrapy.Field()
      cod= scrapy.Field()
      sold_out= scrapy.Field()
      prebook=scrapy.Field()
      rating = scrapy.Field()
      rating_count= scrapy.Field()
      images=scrapy.Field()
      image=scrapy.Field()
      offer_texts= scrapy.Field()
      offer_codes= scrapy.Field()
      excerpts= scrapy.Field()
