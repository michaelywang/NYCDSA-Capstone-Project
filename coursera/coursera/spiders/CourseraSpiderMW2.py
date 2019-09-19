from scrapy import Spider, Request
from scrapy.spiders import SitemapSpider
from coursera.items import CourseraItem
import re
import pandas as pd
import math

class CourseSpider(SitemapSpider):
    name = 'coursera_job_recs_spider' 
    allowed_urls=['https://www.coursera.org']
    sitemap_urls = ['https://www.coursera.org/sitemap~www~courses.xml']
    
    def parse(self,response):
        details = response.xpath('.//div[@class = "rc-MetatagsWrapper"]')
        product_urls = re.sub('>','',re.sub('<200','',str(response))).strip()
        separator = ' '
        
#         try:
#                 star_rating = float(re.findall('(\d+.\d)', str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[0]))[1])
#         except:
#                 star_rating = 'NA'
#         try:
#                 number_ratings = int(re.findall('\d+',re.findall('.\d+ ',str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[1]).replace(",",""))[0])[0])
#         except:
#                 number_ratings= 'NA'
#         try:
#                 number_reviews = int(re.findall('\d+',str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[-1]).replace(",",""))[3])
#         except:
#                 number_reviews = 0
#         try:
#                 recent_views = int(str(details.xpath ('//div[@class="Col_i9j08c-o_O-xsCol12_1m1ceo5"]//div[@class="viewsWithTextOnly_1fs65xr"]//span/text()').extract_first().replace(",","")))
#         except:
#                 recent_views = 0
        try:
                course_name = separator.join(re.findall('\w+',str(details.xpath('.//h1[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s"]//text()').extract())))
        except:
                course_name = 'NA'
#         try:
#                 subtitles = re.sub('Subtitles:','', re.findall('Sub\w.*\w.',str(details.xpath('//div[@class="ProductGlance hideOnLarge_1oaat0b p-t-2"]//div[@class="font-sm text-secondary"]//span/text()').extract()))[0])
#         except:
#                 subtitles = 'NA'
#         try:    
#                 section_type= re.findall('\w+',re.sub('-','',str(details.xpath ('.//div[@class = "BreadcrumbItem_1pp1zxi"]//a/@href').extract()[2])))[1]
#         except:
#                 section_type= 'NA'
#         try:
#                 sub_category =  re.findall('\w+',re.sub('-','',str(details.xpath ('.//div[@class = "BreadcrumbItem_1pp1zxi"]//a/@href').extract()[2])))[2]
#         except:
#                 sub_category = 'NA'
#         try:
#                 skills = details.xpath('.//div[@class = "Skills border-a p-x-2 p-t-1 p-b-2 m-y-2"]//span/text()').extract()
#         except:
#                 skills = 'NA'
#         try:
#                 new_career_share = details.xpath('.//h2[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz m-x-2 m-b-0"]/text()').extract_first()
#         except:
#                 new_career_share = 0
#         try:
#                 career_benefit_share = details.xpath('.//h2[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz m-x-2 m-b-0"]/text()').extract()[2]
#         except:
#                 career_benefit_share = 0
#         try:
#                 hours =  int(re.findall('\d+',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"]/span/text()').re(r'Approx..\w+.*')))[0])
#         except:
#             try:
#                     hours = int(re.findall('\d+',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0 m-t-1s"]/span/text()').re(r'Approx..\w+.*')))[0])
#             except:
#                         hours = 0
#         try:
#                 level = re.findall('\w+(?=\s+Level)',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0 m-t-1s"]//text()').extract()[0]))[0]
#         except:
#             try:
#                     level = re.findall('\w+(?=\s+Level)',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"]//text()').extract()))[0]
#             except:
#                         level = 'NA'
#         try:
#                 university =  re.sub('"','',(re.findall('(title=)(\"(.+?)\")',str(details.xpath('.//div[@class="m-b-1s m-r-1"]').extract())))[0][1])
#         except:
#                 university = 'NA'
#         try:
#                 teacher = details.xpath('.//h3[@class="H2_1pmnvep-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 font-lg"]//text()').extract()[0]
#         except:
#                 teacher = 'NA'
#         try:
#                 summary = details.xpath('.//div[@class ="content-inner"]//text()').extract_first()
#         except:
#                 summary = 'NA'
#         try:
#                 enrollment=response.xpath('//div[@class="rc-ProductMetrics"]//text()').extract()[0]
#         except:
#                 enrollment='NA'
        try:
            job_recs= response.xpath('//div[@class="vertical-box"]//text()').extract()[1:]
        except:
            try:
                job_recs = response.xpath('//ul[@class="roles-section"]//text()').extract()
            except:
                try:
                    job_recs=response.xpath('//div[@class="vertical-box"]//text()').extract()
                except:
                    try:
                        response.xpath('//li[@class="occupation-name"]//text()').extract()
                    except:
                        job_recs='NA'

        item = CourseraItem()
        item['product_urls'] = product_urls
#         item['star_rating'] = star_rating
#         item['number_ratings'] = number_ratings
#         item['number_reviews'] = number_reviews
#         item['recent_views'] = recent_views
        item['course_name'] = course_name
#         item['subtitles'] = subtitles
#         item['section_type'] = section_type
#         item['sub_category'] = sub_category
#         item['skills'] = skills
#         item['new_career_share'] = new_career_share
#         item['career_benefit_share'] = career_benefit_share
#         item['hours'] = hours
#         item['level'] = level
#         item['university'] = university
#         item['teacher'] = teacher
#         item['summary'] = summary
#         item['enrollment'] = enrollment
        item['job_recs'] = job_recs

             

        yield item


              