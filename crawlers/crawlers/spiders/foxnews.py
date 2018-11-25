from scrapy.spiders import SitemapSpider
from crawlers.items import FoxNewsItem
from dateutil.parser import parse
from scrapy.exceptions import CloseSpider

class FoxNewsSpider(SitemapSpider):
    name = 'foxnews'
    allowed_domains = ["www.foxnews.com"]

    sitemap_urls = ['http://www.foxnews.com/sitemap.xml']
    
    def hasXpath(xpath,response):
        response.xpath(xpath)

    def parse(self, response):
        item = FoxNewsItem()
        item['date'] = parse(response.xpath('//meta[@name="dc.date"]/@content').extract()[0], fuzzy=True).date()
        
        # if item['date'] < self.from_date:
        #   raise CloseSpider('sufficient_data_gathered')
        item['url'] = response.url
        try:
            item['author'] = " ".join(response.xpath('//*[@class="article-source"]//text()').extract()).strip()
        except IndexError:
            item['author'] = ''
        item['title'] = response.xpath('//meta[@name="dc.title"]/@content').extract()[0].strip()
        item['description'] = response.xpath('//meta[@name="dc.description"]/@content').extract()[0].strip()


        item['content'] = ' '.join(response.xpath('//*[@class="article-body"]/p//text()').extract()).strip()
        yield item