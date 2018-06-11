import sys
import scrapy
from scrapy import Request, Spider
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class RealSpider(scrapy.Spider):
    name = "reals"
    start_urls = ['https://www.realestate.com.au/neighbourhoods/state/vic']

    driver = webdriver.Chrome()
    driver.get('https://www.realestate.com.au/neighbourhoods/state/vic')
    suburbs = driver.find_elements_by_css_selector('.hero-section a')
    
    def parse(self, response):
        urls = []
        for s in self.suburbs:
            urls.append(s.get_attribute('href'))
    
        for url in urls:
            yield response.follow(url=url, callback=self.parse_price)

        # for url in urls:
        #     print "1231231231: " + url
        # print len(urls)

    def parse_price(self, response):
        # print "123123: " + self.driver.find_elements_by_css_selector('.suburb-name')[0].text
        print response.css('.suburb-name::text').extract()
        # yield {
        #     'SUBURB-NAME': response.css('.suburb-name::text').extract_first(),
        #     'HOUSE-MEDIAN-PRICE': response.css('.price::text').extract_first()
        # }

