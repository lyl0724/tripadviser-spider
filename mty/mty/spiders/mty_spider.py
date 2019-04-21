# -*- coding: utf-8 -*-
import scrapy
from mty.items import CityItem, HotelItem, CommentItem, AroundHotelItem, AroundEatItem, AroundViewItem


class MtySpiderSpider(scrapy.Spider):
    name = 'mty_spider'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/Hotels-g294211-oa20-China-Hotels.html#LEAF_GEO_LIST']

    def __init__(self):
        # 城市item
        self.city_item = CityItem()
        self.city_item['city_name'] = None
        self.city_item['total_hotels'] = None

        # 酒店详情item
        self.hotel_item = HotelItem()
        self.hotel_item['cn_name'] = None
        self.hotel_item['en_name'] = None
        self.hotel_item['hotel_rank'] = None
        self.hotel_item['comment_number'] = None
        self.hotel_item['point'] = None
        self.hotel_item['star'] = None
        self.hotel_item['address'] = None
        self.hotel_item['introduction'] = None
        self.hotel_item['phone'] = None
        self.hotel_item['price'] = None
        self.hotel_item['feature'] = None
        self.hotel_item['reward'] = None
        self.hotel_item['cn_name'] = None
        self.hotel_item['cn_name'] = None
        self.hotel_item['cn_name'] = None

        # 评论页
        self.comment_item = CommentItem()
        self.comment_item['hotel'] = None
        self.comment_item['live_time'] = None
        self.comment_item['comment_time'] = None
        self.comment_item['user'] = None
        self.comment_item['score'] = None
        self.comment_item['title'] = None
        self.comment_item['content'] = None

        # 附近酒店页
        self.aroundhotel_item = AroundHotelItem()
        self.aroundhotel_item['hotel_name'] = None
        self.aroundhotel_item['hotel_distance'] = None
        self.aroundhotel_item['from_name'] = None

        # 附近饭店页
        self.aroundeat_item = AroundEatItem()
        self.aroundeat_item['eat_name'] = None
        self.aroundeat_item['eat_distance'] = None
        self.aroundeat_item['from_name'] = None

        # 附近景点页
        self.aroundview_item = AroundViewItem()
        self.aroundview_item['view_name'] = None
        self.aroundview_item['view_distance'] = None
        self.aroundview_item['from_name'] = None



    def parse(self, response):
        citys = response.xpath("//div[@class='ppr_rup ppr_priv_broad_geo_tiles']/ul[@class='geoList ui_columns is-multiline']//li")
        for city in citys:
            city_item = self.city_item
            name = city.xpath(".//a//div[@class='info']/span[@class='name']/text()").extract_first()[:-2]
            city_item['city_name'] = name
            total_hotels = city.xpath("./a/div[@class='info']/span/span/text()").extract_first()
            city_item['total_hotels'] = int(total_hotels[1 : len(total_hotels) - 1])
            city_url = city.xpath("./a/@href").extract_first()
            url = 'https://www.tripadvisor.cn' + city_url
            yield city_item

            #进下一层，爬酒店url
            yield scrapy.Request(url, callback=self.parse_hotel_url)

            #开始爬下一页的逻辑
            next_link = response.xpath(
                "//div[@class='unified ui_pagination leaf_geo_pagination']//a[@class='nav next taLnk ui_button primary']/@href").extract()
            if next_link:
                next_link = next_link[0]
                yield scrapy.Request("https://www.tripadvisor.cn" + next_link, callback=self.parse)


    def parse_hotel_url(self, response):
        lists = response.xpath("//div[@class='prw_rup prw_meta_hsx_responsive_listing ui_section listItem']")

        for list in lists:
            hotel_url = list.xpath(".//div[@class='listing_title']/a/@href").extract_first()
            url = 'https://www.tripadvisor.cn' + hotel_url
            yield scrapy.Request(url, callback=self.parse_hotel_info)
        next_link = response.xpath("//div[@class='unified ui_pagination standard_pagination ui_section listFooter']//a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://www.tripadvisor.cn" + next_link, callback=self.parse_hotel_url)


    def parse_hotel_info(self, response):
        # 酒店部分的信息爬取
        hotel_item = self.hotel_item
        hotel_item['cn_name'] = response.xpath("//div[@class='ui_column is-12-tablet is-10-mobile hotelDescription']/h1/text()").extract_first()
        hotel_name = response.xpath("//div[@class='ui_column is-12-tablet is-10-mobile hotelDescription']/h1/text()").extract_first()
        hotel_item['en_name'] = response.xpath("//div[@class='ui_column is-12-tablet is-10-mobile hotelDescription']/h1/div/text()").extract_first()
        hotel_rank = response.xpath("//b[@class='rank']/text()").extract_first()
        if hotel_rank == None:
            hotel_item['hotel_rank'] = '暂无排名'
        else:
            hotel_item['hotel_rank'] = hotel_rank
        comment = response.xpath("//span[@class='reviews_header_count']/text()").extract_first()
        if(comment == None):
            hotel_item['comment_number'] = 0
        else:
            comment_number = comment[1 : len(comment) - 1]
            hotel_item['comment_number'] = comment_number
        point_str = response.xpath("//span[@class='overallRating']/text()").extract_first()
        if (point_str == None):
            hotel_item['point'] = 0.0
        else:
            point = float(point_str)
            hotel_item['point'] = point
        hotel_item['star'] = response.xpath("//div[@class='hotels-hotel-review-overview-HighlightedAmenities__amenityItem--3E_Yg']/div/text()").extract_first()
        hotel_item['address'] = response.xpath("//span//span[@class='street-address']/text()").extract_first()
        hotel_item['introduction'] = response.xpath(
            "//div[@class='prw_rup prw_common_responsive_collapsible_text']/span[@class='introText']/text()").extract_first()
        extend = response.xpath(
            "//div[@class='prw_rup prw_common_responsive_collapsible_text']/span[@class='introTextExtension']/text()").extract_first()
        if (extend):
            hotel_item['introduction'] += extend
        hotel_item['phone'] = response.xpath("//span[@class='is-hidden-mobile detail']/text()").extract_first()
        feature = response.xpath(
            "//div[@class='sub_content ui_columns is-multiline is-gapless is-mobile']/div/div[@class='textitem']/text()").extract()
        temp_str = ''
        for i in range(len(feature)):
            temp_str += feature[i]
            if (i != len(feature) - 1):
                temp_str += ', '
        hotel_item['feature'] = temp_str
        reward = response.xpath("//span[@class='ui_icon certificate-of-excellence']/text()").extract_first()
        if reward != None:
            hotel_item['reward'] = reward
        else:
            hotel_item['reward'] = '暂无任何奖项与认可'
        yield hotel_item

        # 评论部分的信息爬取
        hotel_comments = response.xpath("//div[@class='review-container']")
        for hotel_comment in hotel_comments:
            comment_item = self.comment_item
            comment_item['hotel'] = hotel_name
            comment_item['live_time'] = hotel_comment.xpath(".//div[@class='prw_rup prw_reviews_stay_date_hsx']/text()").extract_first()
            comment_item['comment_time'] = hotel_comment.xpath(".//span[@class='ratingDate']/@title").extract_first()
            comment_item['user'] = hotel_comment.xpath(".//div[@class='info_text']/div[1]/text()").extract_first()
            comment_item['score'] = str(int(hotel_comment.xpath('.//div[@class="reviewSelector"]/div/div[2]/span[1]/@class').extract_first()[-2:])/10)
            comment_item['title'] = hotel_comment.xpath(".//span[@class='noQuotes']/text()").extract_first()
            comment_item['content'] = hotel_comment.xpath(".//div[@class='prw_rup prw_reviews_text_summary_hsx']/div/p/text()").extract_first()
            yield comment_item

        # 附近的酒店信息爬取
        hotels_around = response.xpath("//div[@class='grids is-shown-at-tablet']//div[1]//div[@class='ui_columns is-multiline nearbyGrid']")
        for around_hotel in hotels_around:
            aroundhotel_item = self.aroundhotel_item
            aroundhotel_item['hotel_name'] = hotels_around.xpath(".//div[@class='poiName']/text()").extract_first()
            aroundhotel_item['hotel_distance'] = hotels_around.xpath(".//div[@class='distance']/text()").extract_first()
            aroundhotel_item['from_name'] = hotel_name
            yield aroundhotel_item

        # 附近的餐厅信息爬取
        eats_around = response.xpath("//div[@class='grids is-shown-at-tablet']//div[2]//div[@class='ui_columns is-multiline nearbyGrid']")
        for around_eat in eats_around:
            aroundeat_item = self.aroundeat_item
            names = around_eat.xpath(".//div[@class='poiName']/text()").extract()
            for name in names:
                aroundeat_item['eat_name'] = name
                aroundeat_item['from_name'] = hotel_name
            distances = around_eat.xpath(".//div[@class='distance']/text()").extract()
            for distance in distances:
                aroundeat_item['eat_distance'] = distance
            yield aroundeat_item

        # 附近的景点信息爬取
        views_around = response.xpath("//div[@class='grids is-shown-at-tablet']//div[3]//div[@class='ui_columns is-multiline nearbyGrid']")
        for around_view in views_around:
            aroundview_item = self.aroundview_item
            names = around_view.xpath(".//div[@class='poiName']/text()").extract()
            for name in names:
                aroundview_item['view_name'] = name
                aroundview_item['from_name'] = hotel_name
            distances = around_view.xpath(".//div[@class='distance']/text()").extract()
            for distance in distances:
                aroundview_item['view_distance'] = distance
            yield aroundview_item












