import sys
import scrapy
from scrapy import Request, Spider
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('https://www.realestate.com.au/neighbourhoods/state/vic')
suburbs = driver.find_elements_by_css_selector('.hero-section a')
urls = []
for s in suburbs:
    urls.append(s.get_attribute('href'))

class RealSpider(scrapy.Spider):
    name = "reals"
    start_urls = ['https://www.realestate.com.au/neighbourhoods/state/vic']

    def closed(self,spider):
        print("spider closed")
        driver.close()

    def parse(self, response):
        for url in urls:
            yield response.follow(url=url, callback=self.parse_price)

    def parse_price(self, response):
        print response.css('.suburb-name::text').extract_first()
        price = response.css('.price::text').extract()
        unit_price = price[8]
        
        yield {
            'SUBURB-NAME': response.css('.suburb-name::text').extract_first(),
            'HOUSE-MEDIAN-PRICE': response.css('.price::text').extract_first(),
            'UNIT_MEDIAN_PRICE': unit_price
        }
