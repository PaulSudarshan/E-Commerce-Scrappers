import scrapy
import os
# import selectorlib
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
import random



class FlipkartlistingSpider(scrapy.Spider):
    name = 'flipkartListing'
    # allowed_domains = ['flipkart.com']
    page_number = 2
    start_urls = ['https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&otracker[]=categorytree&otracker[]=nmenu_sub_Men_0_T-Shirts&page=1']
    absolute_url=None

    product_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../selectorlib_yaml/flipkart_product.yml'))

    def start_requests(self):

        global absolute_url


        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome('C://Users//Harshavardhan//Downloads//chromedriver.exe',chrome_options=options)

        self.driver.get('https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&otracker[]=categorytree&otracker[]=nmenu_sub_Men_0_T-Shirts&page=1')


        sel = Selector(text=self.driver.page_source)
        urls = sel.css('._2mylT6::attr(href)').extract()
        random.shuffle(urls)
        for url in urls:
            absolute_url = 'https://www.flipkart.com' + url
            yield Request(absolute_url, callback=self.parse_info)
            sleep(2)

        while FlipkartlistingSpider.page_number <25:
            try:
                next_page = self.driver.find_element_by_link_text(str(FlipkartlistingSpider.page_number))
                sleep(3)
                self.logger.info('Sleeping for 3 seconds!')
                next_page.click()
                if FlipkartlistingSpider.page_number <6:
                    FlipkartlistingSpider.page_number += 1

                sel = Selector(text=self.driver.page_source)
                urls = sel.css('._2mylT6::attr(href)').extract()
                for url in urls:
                    absolute_url = 'https://www.flipkart.com' + url

                    yield Request(absolute_url, callback=self.parse_info)
            except NoSuchElementException:
                self.logger.info('No more pages to load!')
                self.driver.quit() # Exit out driver instance
                break


    def parse_info(self, response):
        data = self.product_page_extractor.extract(response.text)
        yield(data)
