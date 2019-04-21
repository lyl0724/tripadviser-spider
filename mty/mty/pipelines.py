# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from mty import settings

class CityPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into city(
                 city_name, total_hotels)
                 value(%s,%s);""",
                (
                 item['city_name'],
                 item['total_hotels'],
                )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item

class HotelPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into hotel(cn_name,
                 en_name, hotel_rank, comment_number, point, star, address, introduction, phone, feature, reward)
                 value(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                 item['cn_name'],
                 item['en_name'],
                 item['hotel_rank'],
                 item['comment_number'],
                 item['point'],
                 item['star'],
                 item['address'],
                 item['introduction'],
                 item['phone'],
                 item['feature'],
                 item['reward']
                 )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item

class CommentPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into comment(hotel, live_time, comment_time, `user`, score, title, content)
                 value(%s,%s,%s,%s,%s,%s,%s)""",
                (
                 item['hotel'],
                 item['live_time'],
                 item['comment_time'],
                 item['user'],
                 item['score'],
                 item['title'],
                 item['content']
                 )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item

class AroundEatPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into around_eat(eat_name, eat_distance, from_name)
                 value(%s,%s,%s)""",
                (
                 item['eat_name'],
                 item['eat_distance'],
                 item['from_name']
                 )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item


class AroundHotelPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into around_hotel(hotel_name, hotel_distance, from_name)
                 value(%s,%s,%s)""",
                (
                 item['hotel_name'],
                 item['hotel_distance'],
                 item['hotel_name']
                 )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item

class AroundViewPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into around_view(view_name, view_distance, from_name)
                 value(%s,%s,%s)""",
                (
                 item['view_name'],
                 item['view_distance'],
                 item['from_name']
                 )
            )
            self.connect.commit()
        except Exception as err:
            print('error: ' + str(err))
            self.connect.rollback()
        return item