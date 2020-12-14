# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException



class HMScraper(Spider):
    name = 'hm_scraper'
    page_number = 2

    start_urls = ['https://www2.hm.com/en_in/men/shop-by-product/view-all.html', 'https://www2.hm.com/en_in/women/shop-by-product/view-all.html']

    def start_requests(self):
        for web_page in self.start_urls:
            self.driver = webdriver.Chrome('chromedriver')
            self.driver.get(web_page)

            sel = Selector(text=self.driver.page_source)

            urls = sel.css('.item-heading .link::attr(href)').extract()

            for url in urls:
                absolute_url = 'https://www2.hm.com' + url
                yield Request(absolute_url, callback=self.parse_info)

            while True:
                try:
                    button = self.driver.find_element_by_class_name('pagination-links-list')
                    sleep(3)
                    self.logger.info('Sleeping for 3 seconds!')
                    self.driver.execute_script("arguments[0].click();", button)

                    sel = Selector(text=self.driver.page_source)

                    urls =  sel.css('.item-heading .link::attr(href)').extract()
                    for url in urls:
                        absolute_url = 'https://www2.hm.com' + url
                        yield Request(absolute_url, callback=self.parse_info)

                except NoSuchElementException:
                    self.logger.info('No more pages to load!')
                    self.driver.quit() # Exit out driver instance
                    break


    #
    def parse_info(self, response):

        prod_name = response.css('.product-item-headline::text').extract_first().strip()
        description = response.css('.pdp-description-text::text').extract_first()
        features_keys = response.css('.pdp-description-list-item dt').css('::text').extract()
        features_values = response.css('.pdp-description-list-item dd').css('::text').extract()
        features_values = [i.strip() for i in features_values]
        features_values = [i for i in features_values if len(i)!=0]
        features = {features_keys[i]: features_values[i] for i in range(len(features_keys))}
        # features['Variant'] = response.css('.product-input-label::text').extract_first()
        price = response.css('.price-value::text').extract_first().strip()
        prod_url = response.url
        img_url = response.css('.pdp-image img::attr(src)').extract_first()

        yield {
                'Product Name': prod_name,
                'Price': price,
                'Features' : features,
                'Product Details' : description,
                'Product Url': prod_url,
                'Image Url' : img_url,
                }

