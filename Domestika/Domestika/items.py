# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

import scrapy

class DomestikaItem(scrapy.Item):
    course_title = scrapy.Field()
    length = scrapy.Field()
    number_students = scrapy.Field()
    positive_reviews_share = scrapy.Field()
    audio = scrapy.Field() 
    reviews = scrapy.Field()
    subtitles = scrapy.Field()
    new_course_date = scrapy.Field()
    price = scrapy.Field()
    dct_price = scrapy.Field()
    discount = scrapy.Field()
    teacher = scrapy.Field()
    teacher_links = scrapy.Field()
    category = scrapy.Field()
    areas = scrapy.Field()
    software = scrapy.Field()
    summary = scrapy.Field()
    level = scrapy.Field()



 