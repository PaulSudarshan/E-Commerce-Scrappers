# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException



class FlipkartSpider(Spider):
    name = 'FlipkartSpider'
    page_number = 2
    # allowed_domains = ['https://www.flipkart.com/search?q=patanjali+products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1']
    start_urls = ['https://www.flipkart.com/search?q=toothpaste&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=1']
    absolute_url=None
    def start_requests(self):

        global absolute_url
        self.driver = webdriver.Chrome('C://Users//Harshavardhan//Downloads//chromedriver.exe')
        self.driver.get('https://www.flipkart.com/search?q=toothpaste&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=1')

        sel = Selector(text=self.driver.page_source)
        urls = sel.css('._2cLu-l::attr(href)').extract()
        for url in urls:
            absolute_url = 'https://www.flipkart.com' + url

            yield Request(absolute_url, callback=self.parse_info)

        while True:
            try:
                next_page = self.driver.find_element_by_link_text(str(FlipkartSpider.page_number))
                sleep(3)
                self.logger.info('Sleeping for 3 seconds!')
                next_page.click()
                if FlipkartSpider.page_number <6:
                    FlipkartSpider.page_number += 1

                sel = Selector(text=self.driver.page_source)
                urls = sel.css('._2cLu-l::attr(href)').extract()
                for url in urls:
                    absolute_url = 'https://www.flipkart.com' + url

                    yield Request(absolute_url, callback=self.parse_info)
            except NoSuchElementException:
                self.logger.info('No more pages to load!')
                self.driver.quit() # Exit out driver instance
                break

    #
    def parse_info(self, response):

        prod_name = response.css('._35KyD6::text').extract_first()[:46]
        prod_brand = prod_name.split(' ')[0]
        price = response.css('._3qQ9m1::text').extract_first()
        category = response.css('._1HEvv0:nth-child(5) ._1KHd47::text').extract_first()
        prod_url =absolute_url
        rating = response.css('._2_KrJI .hGSR34::text').extract()[0]


        yield {
            'Product Name': prod_name,
            'Brand' : prod_brand,
            'Price': price,
            'Category' : category,
            'Product Url': prod_url,
            'rating':rating

                }
