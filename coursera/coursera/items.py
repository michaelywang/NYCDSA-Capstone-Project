# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

import scrapy

class CourseraItem(scrapy.Item):
    # define the fields for your item here like:
    product_urls = scrapy.Field()
#     star_rating = scrapy.Field()
#     number_ratings = scrapy.Field()
#     number_reviews = scrapy.Field()
#     recent_views = scrapy.Field()
    course_name = scrapy.Field() 
#     subtitles = scrapy.Field()
#     section_type = scrapy.Field()
#     sub_category = scrapy.Field()
#     skills = scrapy.Field()
#     new_career_share = scrapy.Field() 
#     career_benefit_share = scrapy.Field() 
#     hours = scrapy.Field() 
#     level = scrapy.Field() 
#     university = scrapy.Field() 
#     teacher = scrapy.Field() 
#     summary = scrapy.Field()
#     enrollment = scrapy.Field()
    job_recs = scrapy.Field()
 