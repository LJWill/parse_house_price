import sys
import scrapy
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
        for s in self.suburbs: 
            yield response.follow(s.get_attribute('href'), callback=self.parse_price)
            
    def parse_price(self, response):
        try: 
            suburb_name = self.driver.find_elements_by_css_selector('.suburb-name')[0].text
            house_price = self.driver.find_elements_by_css_selector('.price')[0].text
        except IndexError:
            print "index error!!!!!!"
        yield {
            'SUBURB-NAME': suburb_name,
            'HOUSE-MEDIAN-PRICE': house_price,
        }

