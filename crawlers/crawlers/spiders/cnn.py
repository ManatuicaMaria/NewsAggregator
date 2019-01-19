from scrapy.spiders import SitemapSpider, Spider
from crawlers.items import NewsItem
from dateutil.parser import parse
from crawlers.spiders.utils import remove_unicode


class CNNSpider(SitemapSpider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    sitemap_urls = ['https://www.cnn.com/sitemaps/cnn/index.xml']

    def parse(self, response):
        article = response.xpath('//article[@itemtype="https://schema.org/NewsArticle"]')
        if article is None:
            return

        item = NewsItem()

        item['url'] = article.xpath('//meta[@itemprop="url"]/@content').extract_first()
        if item['url'] is None:
            return

        title = article.xpath('//meta[@itemprop="headline"]/@content').extract_first()
        if title is None:
            return

        index = title.index(' - CNN')
        if index >= 0:
            title = title[0:index]

        item['title'] = remove_unicode(title)

        item['description'] = remove_unicode(article.xpath('//meta[@itemprop="description"]/@content').extract_first())
        if item['description'] is None:
            return

        date = article.xpath('//meta[@itemprop="dateCreated"]/@content').extract_first()
        if date is None:
            return

        item['date'] = parse(date).strftime("%Y-%m-%dT%H:%M:%S")
        if item['date'] is None:
            return

        item['author'] = remove_unicode(article.xpath('//meta[@itemprop="author"]/@content').extract_first())
        if item['author'] is None:
            return

        articleBody = response.xpath('//article[@itemprop="articleBody"]')
        if articleBody is None:
            return

        paragraphs = response.xpath('//div[@class="zn-body__paragraph speakable"]')
        paragraphs.extend(response.xpath('//div[@class="zn-body__paragraph"]'))
        if len(paragraphs) == 0:
            return

        content = []
        for p in paragraphs:
            content.extend(p.xpath('string()').extract())

        item['content'] = remove_unicode(' '.join(content))

        yield item