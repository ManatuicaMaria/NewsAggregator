# -*- coding: utf-8 -*-
import scrapy


class InfowarsSpider(scrapy.Spider):
    name = 'infowars'
    allowed_domains = ['www.infowars.com']
    start_urls = ['http://www.infowars.com/']

    def parse(self, response):
        # TODO: Add logic    
        pass
