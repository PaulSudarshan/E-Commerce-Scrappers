# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
import time
from selenium.common.exceptions import NoSuchElementException
from scrapy.utils.response import open_in_browser


class MyntraSpider(Spider):
    name = 'myntra_scraper'
    page_number = 2
    # allowed_domains = ['www.myntra.com']
    start_urls = ['https://www.myntra.com/men-tshirts?p=1','https://www.myntra.com/trousers?p=1']
    absolute_url=None
    def start_requests(self):
        for web_page in self.start_urls:

            self.driver = webdriver.Chrome('chromedriver')
            self.driver.get(web_page)

            links=[]
            n=0
            while n<1:
                n=n+1
                for product_base in self.driver.find_elements_by_class_name('product-base'):
                    try:
                        links.append(product_base.find_element_by_xpath('./a').get_attribute("href"))
                    except:
                        continue
                try:
                    self.driver.find_element_by_class_name('pagination-next').click()
                except:
                    self.driver.close()
                    self.driver.quit()

            print(links)
            for url in links:
                yield Request(url, callback=self.parse_info)


    def parse_info(self, response):
        # self.driver = webdriver.Chrome('C://Users//sudar//Downloads//Compressed//chromedriver')
        self.driver.get(response.url)
        sel = Selector(text=self.driver.page_source)
        metadata = {}
        metadata['Brand'] = self.driver.find_element_by_class_name('pdp-title').get_attribute("innerHTML")
        metadata['Product Name'] = self.driver.find_element_by_class_name('pdp-name').get_attribute("innerHTML")
        metadata['Price'] = self.driver.find_element_by_class_name('pdp-price').find_element_by_xpath('./strong').get_attribute("innerHTML")
        metadata['Image_Url'] = sel.xpath('//meta[@itemprop="image"]/@content').extract()  # to get the xpath of image location
        metadata['Discount'] = sel.css('.pdp-discount::text').extract_first()
        metadata['Coupon'] = sel.css('.pdp-offers-boldText::text').extract_first()
        details = sel.css('.index-row div::text').extract()
        metadata['Specifications'] = {details[i]: details[i + 1] for i in range(0, len(details), 2)}
        metadata['Previous Price'] = ''.join(sel.css('.pdp-mrp s::text').extract())

        try:
            self.driver.find_element_by_class_name('index-showMoreText').click()
        except:
            print('error')
        for index_row in self.driver.find_element_by_class_name('index-tableContainer').find_elements_by_class_name('index-row'):
            # metadata['Specifications'] = index_row.find_element_by_class_name('index-rowKey').get_attribute("innerHTML") +'-'+ index_row.find_element_by_class_name('index-rowValue').get_attribute("innerHTML")
            metadata['productId'] = self.driver.find_element_by_class_name('supplier-styleId').get_attribute("innerHTML")

        yield metadata

