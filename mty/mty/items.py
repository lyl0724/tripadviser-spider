# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    city_name = scrapy.Field()
    total_hotels = scrapy.Field()

class HotelItem(scrapy.Item):
    cn_name = scrapy.Field()
    en_name = scrapy.Field()
    hotel_rank = scrapy.Field()
    comment_number = scrapy.Field()
    point = scrapy.Field()
    star = scrapy.Field()
    address = scrapy.Field()
    introduction = scrapy.Field()
    phone = scrapy.Field()
    price = scrapy.Field()
    feature = scrapy.Field()
    reward = scrapy.Field()
    hotel_id = scrapy.Field()
    price = scrapy.Field()

class CommentItem(scrapy.Item):
    hotel = scrapy.Field()
    live_time = scrapy.Field()
    comment_time = scrapy.Field()
    user = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class AroundHotelItem(scrapy.Item):
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_distance = scrapy.Field()
    from_name = scrapy.Field()

class AroundEatItem(scrapy.Item):
    eat_name = scrapy.Field()
    eat_distance = scrapy.Field()
    from_name = scrapy.Field()

class AroundViewItem(scrapy.Item):
    view_name = scrapy.Field()
    view_distance = scrapy.Field()
    from_name = scrapy.Field()

