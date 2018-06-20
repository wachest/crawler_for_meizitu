# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem

class MztSpider(scrapy.Spider):
    name = 'mzt'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
 
    	# 指向二级页面并解析
    	for href in response.css('ul.wp-list li.wp-item h3.tit a::attr(href)'):
    		yield response.follow(href, self.parse_second_page)

    	# 回调一级页面并解析
    	for index in range(1, 72):
    		next_page = 'more_%s.html' % index
    		yield response.follow(next_page, callback=self.parse)

    def parse_second_page(self, response):
    	item = MeizituItem()
    	image_urls = response.css('div.postContent img::attr(src)').extract()
    	image_folder_name = response.css('div.postmeta a::text').extract_first()
    	item['image_folder_name'] = image_folder_name
    	item['image_urls'] = image_urls
    	yield item


