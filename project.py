from ..items import FlipkartItem
import json
import scrapy
import re


class FlipkartscrapySpider(scrapy.Spider):
    name = 'flipkartscrapy'

    def start_requests(self):
        urls = ['https://www.flipkart.com/clothing-and-accessories/topwear/pr?sid=clo%2Cash&otracker=categorytree&p%5B%5D=facets.ideal_for%255B%255D%3DMen&page={}',
        'https://www.flipkart.com/womens-footwear/pr?sid=osp%2Ciko&otracker=nmenu_sub_Women_0_Footwear&page={}']

        for url in urls:
            for i in range(1,25):
                x = url.format(i)
                yield scrapy.Request(url=x, callback=self.parse)


    def parse(self, response):
        items = FlipkartItem()
        name = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "IRpwTa", " " ))]').xpath('text()').getall()
        brand = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_2WkVRV", " " ))]').xpath('text()').getall()
        original_price = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_3I9_wc", " " ))]').xpath('text()').getall()
        sale_price = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_30jeq3", " " ))]').xpath('text()').getall()
        image_url = response.css('._1a8UBa').css('::attr(src)').getall()
        product_page_url =response.css('._13oc-S > div').css('::attr(href)').getall()

        items['name'] = name
        items['brand'] = brand
        items['original_price'] = original_price
        items['sale_price'] = sale_price
        items['image_url'] = image_url
        items['product_page_url'] = 'https://www.flipkart.com' + str(product_page_url)
         
        yield items