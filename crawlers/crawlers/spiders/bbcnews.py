from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem

from datetime import datetime
from utils import remove_unicode


class BBCNewsSpider(SitemapSpider):
    name = 'bbcnews'
    allowed_domains = ["www.bbc.com", "www.bbc.co.uk"]

    sitemap_urls = ['https://www.bbc.co.uk/robots.txt']

    def hasXpath(xpath, response):
        response.xpath(xpath)

    def parse(self, response):
        item = NewsItem()

        lang = response.xpath(
            '//*[@id="responsive-news"]//meta[@property="og:locale"]//@content').extract_first()

        type = response.xpath(
            '//*[@id="responsive-news"]//meta[@property="og:type"]//@content').extract_first()

        if lang is None or "en" not in lang or "article" not in type:
            return

        item['url'] = response.url

        try:
            item['date'] = datetime.utcfromtimestamp(float(
                response.xpath(
                    '//div[@class="story-body"]//div[contains(@class,"date date--v2")]//@data-seconds').extract_first())).strftime(
                "%Y-%m-%d %H:%M:%S")
        except TypeError:
            item['date'] = ''
        try:
            item['author'] = " ".join(
                response.xpath('//*[@id="responsive-news"]//meta[@property="article:author"]//@content')
                    .extract()[0]).strip()
        except IndexError:
            item['author'] = ''
        item['title'] = response.xpath(
            '//*[@id="responsive-news"]//meta[@property="og:title"]//@content').extract_first().strip()

        item['description'] = response.xpath(
            '//*[@id="responsive-news"]//meta[@property="og:description"]//@content').extract_first().rstrip()

        item['content'] = remove_unicode(' '.join(response.xpath(
            '//div[@class="story-body"]//div[@property="articleBody"]//p//text()').extract()).rstrip())

        yield item
