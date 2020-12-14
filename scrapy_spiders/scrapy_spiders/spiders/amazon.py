# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException



class AmazonSpider(Spider):
    name = 'amazon_scraper'
    page_number = 2

    start_urls = ['https://www.amazon.in/s?k=T-SHIRTS+AND+POLOS&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Shirts&i=fashion&rh=n%3A7459781031&page=1','https://www.amazon.in/s?k=Trouser&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Jeans&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Innerwear&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Sportswear&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=SLEEP+%26+LOUNGE+WEAR&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Ethnic+Wear&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=ties+socks+and+belts&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Suits+and+Blazers&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Sweaters&i=fashion&rh=n%3A7459781031&page=1','https://www.amazon.in/s?k=Jackets+and+Coats&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Shoes&i=fashion&rh=n%3A7459781031&page=1','https://www.amazon.in/s?k=Watches&i=fashion&rh=n%3A7459781031&page=1','https://www.amazon.in/s?k=Jewellery&i=fashion&rh=n%3A7459781031&page=1', 'https://www.amazon.in/s?k=Eyewear&i=fashion&rh=n%3A7459781031&page=1','https://www.amazon.in/s?k=Clothing&i=fashion&rh=n%3A7459780031&page=1','https://www.amazon.in/s?k=Shoes&i=fashion&rh=n%3A7459780031&page=1','https://www.amazon.in/s?k=Eyewear&i=fashion&rh=n%3A7459780031&page=1','https://www.amazon.in/s?k=Watches&i=fashion&rh=n%3A7459780031&page=1','https://www.amazon.in/s?k=Jewellery&i=fashion&rh=n%3A7459780031&page=1', 'https://www.amazon.in/s?k=Handbaga+and+clutches&i=fashion&rh=n%3A7459780031&page=1']

    category_no=0
    def start_requests(self):
        for web_page in self.start_urls:
            self.driver = webdriver.Chrome('chromedriver')
            self.driver.get(web_page)

            sel = Selector(text=self.driver.page_source)

            urls = sel.css('.a-link-normal.a-text-normal::attr(href)').extract()
            for url in urls:
                absolute_url = 'https://www.amazon.in' + url
                yield Request(absolute_url, callback=self.parse_info)

            while True:
                try:
                    self.driver.get('https://www.amazon.in/s?k=shirts&page='+str(AmazonSpider.page_number))
                    # next_page.click()
                    if AmazonSpider.page_number <= 3:
                        AmazonSpider.page_number += 1
                    else:
                        raise NoSuchElementException

                    sel = Selector(text=self.driver.page_source)

                    urls = sel.css('.a-link-normal.a-text-normal::attr(href)').extract()
                    for url in urls:
                        absolute_url = 'https://www.amazon.in' + url
                        yield Request(absolute_url, callback=self.parse_info)

                except NoSuchElementException:
                    self.logger.info('No more pages to load!')
                    self.driver.quit() # Exit out driver instance
                    break


    #
    def parse_info(self, response):

        prod_name = response.css('#productTitle::text').extract_first()
        prod_brand = response.css('#bylineInfo::text').extract_first()
        price = response.css('#priceblock_ourprice::text').extract_first()
        features = response.css('#feature-bullets .a-list-item::text').extract()
        prod_url = response.url
        img_url = response.css('span .a-declarative img::attr(src)').extract()[1]
        rating = response.css('span.a-icon-alt::text').extract_first()
        discount =  response.css('.priceBlockSavingsString::text').extract_first()
        details = response.css('#detailBullets_feature_div span::text').extract()
        yield {
                'Product Name': prod_name,
                 'Brand' : prod_brand,
                'Price': price,
                'Features' : features,
                'Product Details' : details,
                'Product Url': prod_url,
                'Image Url' : img_url,
                'Discount Offered' : discount,
                'rating':rating
                }

