# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem
from dateutil.parser import parse
import re

class InfowarsSpider(scrapy.Spider):
    name = "infowars"
    allowed_domains = ['www.infowars.com']
    base_url = "http://www.infowars.com"
    start_urls = ["http://www.infowars.com/news/"]
    max_pages_per_category = 10
    
    def get_pages(self, href):
        url = href if "http" in href else self.get_absolute_url(href)
        return ['{0}page/{1}/'.format(url, str(page + 1)) for page in range(self.max_pages_per_category)]
             
    def get_absolute_url(self, href):
        return '{0}{1}'.format(self.base_url, href)
    
    def parse(self, response):
        for href in response.xpath('//li[contains(@class, "current_page_item")]//li//a/@href').extract():
            for url in self.get_pages(href):
                yield scrapy.Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        for href in response.xpath('//div[@class="article-content"]//a/@href').extract():
            yield scrapy.Request(url=href, callback=self.parse_item_page)

    def parse_item_page(self, response):
        item_data = {
            "title": self.remove_unicode(response.xpath('//meta[@property="og:title"]/@content').extract()[0].strip()),
            "author": " ".join(response.xpath('//span[@class="author"]//text()').extract()[1:-1]).strip(),
            "date": parse(response.xpath('//meta[@property="article:published_time"]/@content').extract()[0].strip(), fuzzy=True).date(),
            "description": self.remove_unicode(response.xpath('//meta[@property="og:description"]/@content').extract()[0].strip()),
            "content": self.get_content(response),
            "url": response.url,
        }
        yield NewsItem(**item_data)

    def get_content(self, response, string="SUBSCRIBE"):
        ps = response.xpath('//article//p//*[not(self::script)]//text()').extract()
        if string in ps:
            ps = ps[:ps.index(string)]
        ps = map(lambda s: s.strip(), ps)
        return self.remove_unicode(" ".join(ps).strip())

    def remove_unicode(self, s):
        return s.encode('ascii', 'ignore')