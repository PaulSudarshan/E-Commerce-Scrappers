# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException



class FlipkartSpider(Spider):
    name = 'scraper'
    page_number = 2
    # allowed_domains = ['https://www.flipkart.com/search?q=patanjali+products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1']
    start_urls = ['https://www.flipkart.com/search?q=micromax+smartphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1']

    def start_requests(self):
        for i in self.start_urls:
            self.driver = webdriver.Chrome('chromedriver')
            self.driver.get(i)

            sel = Selector(text=self.driver.page_source)
            urls = sel.css('._3dqZjq::attr(href)').extract()
            if len(urls)==0:
                urls = sel.css('._2mylT6::attr(href)').extract()
            if len(urls)==0:
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
                    if FlipkartSpider.page_number <3:
                        FlipkartSpider.page_number += 1
                    else:
                        raise NoSuchElementException

                    for url in urls:
                        absolute_url = 'https://www.flipkart.com' + url
                        yield Request(absolute_url, callback=self.parse_info)

                except NoSuchElementException:
                    self.logger.info('No more pages to load!')
                    self.driver.quit() # Exit out driver instance
                    break

    #
    def parse_info(self, response):
        prod_name = response.css('._35KyD6::text').extract()
        prod_brand = response.css('._2J4LW6::text').extract()
        price = response.css('._3qQ9m1::text').extract()
        category = response.css('._1HEvv0:nth-child(4) ._1KHd47::text').extract()
        prod_url =response.url
        rating = response.css('.bqXGTW::text').extract()
        img_url = response.css('._3togXc::attr(src)').extract_first()
        offers =  response.css('._2-n-Lg span::text').extract()
        reviews = response.css('._2nc08B span::text').extract_first()

        features = response.css('._2t27J6 .col::text').extract()
        features = {features[i] : features[i+1] for i in range(0,len(features),2)}
        yield {
                'Product Name': prod_name,
                 'Brand' : prod_brand,
                'Price': price,
                'Category' : category,
                'Product Url': prod_url,
                'Rating':rating,
                'Image_Url':img_url,
                'Offers' : offers,
                'Total Reviews' : reviews,
                'Features' : features

                }

