from scrapy.spiders import SitemapSpider, Spider
from crawlers.items import NewsItem
from dateutil.parser import parse

class TheTelegraphSpider(SitemapSpider):

    name = 'telegraph'
    allowed_domains = ['www.telegraph.co.uk']
    sitemap_urls = ['https://www.telegraph.co.uk/news/sitemap.xml']

    def parse(self, response):
        article = response.xpath('/html/head/meta[@property="og:type" and @content="article"]')
        if article is None:
            return

        item = NewsItem()

        item['url'] = response.xpath('//meta[@property="og:url"]/@content').extract_first()
        if item['url'] is None:
            return

        item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        if item['title'] is None:
            return

        item['description'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        if item['description'] is None:
            return

        date = response.xpath('//*[@itemprop="datePublished"]/@content').extract_first()
        if date is None:
            return

        item['date'] = parse(date)
        if item['date'] is None:
            return

        author = response.xpath('//*[@class="article-author"]')
        if author is None:
            return
        item['author'] = ' '.join(response.xpath('//*[@class="byline__author-name" and @itemprop="name"]/@content').extract())
        if item['author'] is None:
            return

        articleBody = response.xpath('//article[@itemprop="articleBody"]')
        if articleBody is None:
            return

        content = []
        paragraphs = articleBody.xpath('//div[@class="article-body-text component version-2"]//p')
        if len(paragraphs) == 0:
            print('no paragraphs for ' + item['title'])
            return

        for p in paragraphs:
            content.extend(p.xpath('string()').extract())

        item['content'] = ' '.join(content)

        yield item