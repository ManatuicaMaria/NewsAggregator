from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem
from dateutil.parser import parse


class AbcNewsSpider(SitemapSpider):
    name = 'abcnews'
    allowed_domains = ["abcnews.go.com"]

    sitemap_urls = ['https://abcnews.go.com/robots.txt']

    def hasXpath(xpath, response):
        response.xpath(xpath)

    def parse(self, response):
        item = NewsItem()

        type = response.xpath('//meta[@property="og:type"]//@content').extract_first()

        if "article" not in type:
            return

        item['url'] = response.url
        item['date'] = parse(
            response.xpath('//*[@id="article-feed"]/article[1]//span[@class="timestamp"]').extract()[0],
            fuzzy=True)

        try:
            item['author'] = " ".join(
                response.xpath('//*[@id="article-feed"]/article[1]//div[@class="author"]//text()')
                    .extract()).strip()
        except IndexError:
            item['author'] = ''
        item['title'] = response.xpath('//meta[@property="og:title"]//@content').extract()[0].strip()
        item['description'] = response.xpath(
            '//meta[@property="og:description"]//@content').extract_first().rstrip()

        item['content'] = ' '.join(response.xpath(
            '//*[@id="article-feed"]/article[1]//*[@class="article-body"]//*[@itemprop="articleBody"]//text()').extract()).rstrip()
        yield item
