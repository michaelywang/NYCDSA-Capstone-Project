from scrapy import Spider, Request
from Domestika.items import DomestikaItem
import re
import pandas as pd

class DomestikaSpider(Spider):
    name = 'Domestika_Spider'
    allowed_urls = ['https://www.domestika.org/en/']
    start_urls = ['https://www.domestika.org/en/courses']


    def parse(self,response):
        urls = response.xpath('.//ul[@class="nav nav--lateral"]//a/@href').extract()
        urls = pd.Series(urls)
        filter_cat = urls.str.contains('category', regex=False)
        urls = urls[filter_cat]
        urls = list(urls)

        for url in urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page (self,response):
        product_urls = response.xpath('.//ul[@class = "row courses-list-boxed js-courses-wrapper"]//div[@class ="course-item__details"]//a/@href').extract()


        for url in product_urls:
            yield Request(url=url, callback=self.parse_detail_page)

        ## surface important information at this level
    def parse_detail_page (self,response):

        details =  response.xpath('//main[@class="js-main-content"]') 

        for detail in details:

            try:
                course_title = details.xpath('.//h1[@class = "h2 hero--course__title"]//text()').extract()[1]
            except:
                course_title = 'NA'
            try:    
                length = list(filter(lambda x: re.findall('^[0-9]+h [0-9]+m$', x), list(map(str.lstrip,details.xpath('//li[@class="list-inline-item"]/text()').extract()))))[0]
            except:
                length = 'NA'
            try:
                number_students = int(list(filter(lambda x: re.findall('^[0-9]+$', x), list(map(str.lstrip,details.xpath('//li[@class="list-inline-item"]/text()').extract()))))[0])
            except:
                number_students = 0
            try:           
                positive_reviews_share = int(re.findall('\d+',list(filter(lambda x: re.findall('([0-9]\%)', x), list(map(str.lstrip,details.xpath('//li[@class="list-inline-item"]/text()').extract()))))[0])[0])
            except:
                positive_reviews_share = 0
            try:
                audio = list(filter(lambda x: re.findall('^Audio: +', x), list(map(str.lstrip,details.xpath('//li[@class="list-inline-item"]/text()').extract()))))[0].split(': ')[1]
            except:
                audio = 'NA'
            try:
                subtitles = list(filter(lambda x: re.findall('^Audio: +', x), list(map(str.lstrip,details.xpath('//li[@class="list-inline-item"]/text()').extract()))))[0].split(': ')[1]
            except:
                subtitles = 'NA'
            try:
                reviews = int(re.findall('\d+',str(details.xpath('.//div[@id="comments"]//h5/text()[2]')))[2])
            except:
                reviews = 0
            try:
                new_course_date = re.findall('\d+.[a-z].+',details.xpath('//div[@class="col-md-3"]//ul[@class = "item-stats course-stats"]//li/a/text()').extract()[0])[0]
            except:
                new_course_date = 'No new course'
            try:
                price = list(filter(lambda x: re.findall('\d+', x),list(map(str.lstrip,details.xpath('.//span[@class = "price-badges--prices"]//text()').extract()))))[1]
            except:
                price = 'NA'
            try:
                dct_price = list(map(str.strip,details.xpath('.//div[@class ="hero__price-and-savings hero__price-and-savings--with-retail"]//text()').extract()))[1]
            except:
                dct_price = 'NA'
            try:
                discount = list(filter(lambda x: re.findall('\d+', x),list(map(str.lstrip,details.xpath('.//span[@class = "price-badges--prices"]//text()').extract()))))[0]
            except:
                discount = 'NA'
            try:
                teacher =  list(map(str.lstrip,details.xpath('.//h3[@class = "course-teacher__name"]//text()').extract()))[1]
            except:
                teacher = 'NA'
            try:
                teacher_links = details.xpath('.//div[@class = "d-flex align-items-center"]//a/@href').extract()
            except:
                teacher_links = 'NA'
            try:
                category = list(map(str.strip,details.xpath('.//div[@class = "section course-categories"]//text()').extract()))[3]
            except:
                category = 'NA'
            try:
                areas = list(map(str.strip,details.xpath('.//div[@class = "section course-areas"]//text()').extract()))[3:]
            except:
                areas = 'NA'
            try:
                software = list(map(str.strip,details.xpath('.//div[@class = "section course-softwares"]//text()').extract()))[3:]
            except:
                software = 'NA'
            try:
                summary =  re.sub('\\n\\n','',re.sub('<.*?>','',str(details.xpath('.//div[@class = "includes"]').extract())))
            except:
                summary = 'NA'
            try:
                level = details.xpath('.//li[@class = "course-level"]//text()').extract()[2]
            except:
                level = 'NA'  


            item = DomestikaItem()
            item['course_title'] = course_title
            item['length'] = length
            item['number_students'] = number_students
            item['positive_reviews_share'] = positive_reviews_share
            item['audio'] = audio
            item['subtitles'] = subtitles
            item['reviews'] = reviews
            item['new_course_date'] = new_course_date
            item['price'] = price
            item['dct_price'] = dct_price
            item['discount'] = discount
            item['teacher'] = teacher
            item['teacher_links'] = teacher_links
            item['category'] = category
            item['areas'] = areas
            item['software'] = software
            item['summary'] = summary
            item['level'] = level


            yield item



 

             


             


