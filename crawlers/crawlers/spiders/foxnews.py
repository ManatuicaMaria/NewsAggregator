from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem
from dateutil.parser import parse
from utils import remove_unicode


class FoxNewsSpider(SitemapSpider):
    name = 'foxnews'
    allowed_domains = ["www.foxnews.com"]
    sitemap_urls = ['http://www.foxnews.com/sitemap.xml']

    def hasXpath(xpath, response):
        response.xpath(xpath)

    def parse(self, response):
        item_data = {
            "title": remove_unicode(response.xpath('//meta[@name="dc.title"]/@content').extract()[0].strip()),
            "author": " ".join(response.xpath('//*[@class="article-source"]//text()').extract()).strip(),
            "date": parse(response.xpath('//meta[@name="dc.date"]/@content').extract()[0], fuzzy=True).strftime(
                "%Y-%m-%dT%H:%M:%S"),
            "description": remove_unicode(
                response.xpath('//meta[@name="dc.description"]/@content').extract()[0].strip()),
            "content": remove_unicode(
                ' '.join(response.xpath('//*[@class="article-body"]/p//text()').extract()).strip()),
            "url": response.url,
        }
        yield NewsItem(**item_data)
