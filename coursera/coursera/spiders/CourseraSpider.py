from scrapy import Spider, Request
from coursera.items import CourseraItem
import re
import pandas as pd
import math

class CourseraSpider(Spider):
    name = 'CourseraSpider'
    allowed_urls = ['https://www.coursera.org']
    start_urls = ['https://www.coursera.org/search?query=data%20science&']

    def parse(self,response):
        details =   response.xpath('//div[@class ="Box_120drhm-o_O-startJustify_5bl4d6-o_O-startAlign_jd8lz2-o_O-displayflex_poyjc mega-menu"]//a/@href').extract()
        details = [i.replace('/browse/', '').replace('-',' ').replace('/degrees','').replace('/browse','') for i in details]
        details = [item for item in details if item != '']
        details = [i.replace(' ', '%20') for i in details]
        url_landing = ['https://www.coursera.org/courses?query={}'.format(x) for x in details]

        for url in url_landing[:2]:
            yield Request(url=url, callback=self.parse_category_page)


    def parse_category_page (self,response):
        num_courses = int(re.findall('\d+',str(response.xpath('.//div[@class= "filter-menu-and-number-of-results horizontal-box"]//span/text()').extract()))[0])
        pages = min(math.ceil(num_courses/10),100)
        course = re.findall('".*"',str(response.xpath('.//div[@class= "filter-menu-and-number-of-results horizontal-box"]//span/text()').extract()))[0].replace('"','').replace(' ', '%20')
        url_list = ['https://www.coursera.org/courses?query={}&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bpage%5D={}&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_custom_ranking_revenuelast28d%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true'.format(course,x) for x in range(pages)]
        
        for url in url_list:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page (self,response):
        product_urls = response.xpath('.//ul[@class ="ais-InfiniteHits-list"]/li[@class = "ais-InfiniteHits-item"]//a/@href').extract()
        product_urls = pd.Series(product_urls)
        filter_cat =   product_urls.str.contains('learn', regex=False)
        product_urls = list(product_urls[filter_cat])
        product_urls = ['https://www.coursera.org'+ s for s in product_urls]

        for url in product_urls:
            yield Request(url=url, callback=self.parse_detail_page)

    def parse_detail_page (self,response):
        details = response.xpath('.//div[@class = "rc-MetatagsWrapper"]')
        product_urls = re.sub('>','',re.sub('<200','',str(response))).strip()
        separator = ' '

        
        for detail in details:
            try:
                star_rating = float(re.findall('(\d+.\d)', str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[0]))[1])
            except:
                star_rating = 'NA'
            try:
                number_ratings = int(re.findall('\d+',re.findall('.\d+ ',str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[1]).replace(",",""))[0])[0])
            except:
                number_ratings= 'NA'
            try:
                number_reviews = int(re.findall('\d+',str(details.xpath ('.//div[@class = "courseRatingContainer_1g3e6m"]//span/text()')[-1]).replace(",",""))[3])
            except:
                number_reviews = 0
            try:
                recent_views = int(str(details.xpath ('//div[@class="Col_i9j08c-o_O-xsCol12_1m1ceo5"]//div[@class="viewsWithTextOnly_1fs65xr"]//span/text()').extract_first().replace(",","")))
            except:
                recent_views = 0
            try:
                course_name = separator.join(re.findall('\w+',str(details.xpath('.//h1[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s"]//text()').extract())))
            except:
                course_name = 'NA'
            try:
                subtitles = re.sub('Subtitles:','', re.findall('Sub\w.*\w.',str(details.xpath('//div[@class="ProductGlance hideOnLarge_1oaat0b p-t-2"]//div[@class="font-sm text-secondary"]//span/text()').extract()))[0])
            except:
                subtitles = 'NA'
            try:    
                section_type= re.findall('\w+',re.sub('-','',str(details.xpath ('.//div[@class = "BreadcrumbItem_1pp1zxi"]//a/@href').extract()[2])))[1]
            except:
                section_type= 'NA'
            try:
                sub_category =  re.findall('\w+',re.sub('-','',str(details.xpath ('.//div[@class = "BreadcrumbItem_1pp1zxi"]//a/@href').extract()[2])))[2]
            except:
                sub_category = 'NA'
            try:
                skills = details.xpath('.//div[@class = "Skills border-a p-x-2 p-t-1 p-b-2 m-y-2"]//span/text()').extract()
            except:
                skills = 'NA'
            try:
                new_career_share = details.xpath('.//h2[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz m-x-2 m-b-0"]/text()').extract_first()
            except:
                new_career_share = 0
            try:
                career_benefit_share = details.xpath('.//h2[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz m-x-2 m-b-0"]/text()').extract()[2]
            except:
                career_benefit_share = 0
            try:
                hours =  int(re.findall('\d+',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"]/span/text()').re(r'Approx..\w+.*')))[0])
            except:
                try:
                    hours = int(re.findall('\d+',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0 m-t-1s"]/span/text()').re(r'Approx..\w+.*')))[0])
                except:
                        hours = 0
            try:
                level = re.findall('\w+(?=\s+Level)',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0 m-t-1s"]//text()').extract()[0]))[0]
            except:
                try:
                    level = re.findall('\w+(?=\s+Level)',str(details.xpath('//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"]//text()').extract()))[0]
                except:
                        level = 'NA'
            try:
                university =  re.sub('"','',(re.findall('(title=)(\"(.+?)\")',str(details.xpath('.//div[@class="m-b-1s m-r-1"]').extract())))[0][1])
            except:
                university = 'NA'
            try:
                teacher = details.xpath('.//h3[@class="H2_1pmnvep-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 font-lg"]//text()').extract()[0]
            except:
                teacher = 'NA'
            try:
                summary = details.xpath('.//div[@class ="content-inner"]//text()').extract_first()
            except:
                summary = 'NA'
            try:
                enrollment=response.xpath('//div[@class="rc-ProductMetrics"]//text()').extract()[0]
            except:
                enrollment='NA'
            try:
                job_recs = response.xpath('//ul[@class="roles-section"]//text()').extract()
            except:
                job_recs='NA'

            item = CourseraItem()
            item['product_urls'] = product_urls
            item['star_rating'] = star_rating
            item['number_ratings'] = number_ratings
            item['number_reviews'] = number_reviews
            item['recent_views'] = recent_views
            item['course_name'] = course_name
            item['subtitles'] = subtitles
            item['section_type'] = section_type
            item['sub_category'] = sub_category
            item['skills'] = skills
            item['new_career_share'] = new_career_share
            item['career_benefit_share'] = career_benefit_share
            item['hours'] = hours
            item['level'] = level
            item['university'] = university
            item['teacher'] = teacher
            item['summary'] = summary
            item['enrollment'] = enrollment
            item['job_recs'] = job_recs

             

            yield item


              