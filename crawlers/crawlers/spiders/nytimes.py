from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem
from dateutil.parser import parse
from crawlers.spiders.utils import remove_unicode


class NytSpider(SitemapSpider):
    name = 'nytimes'
    allowed_domains = ['www.nytimes.com']
    # not sure if this could be used: https://spiderbites.nytimes.com/
    # Using the previous sitemap "https://www.nytimes.com/sitemaps/www.nytimes.com/sitemap.xml.gz"
    # was taking too long to find a number of articles, and they were very old
    # We could also use https://www.nytimes.com/sitemaps/www.nytimes.com/2016_election_sitemap.xml.gz
    # since our training data sets for the model included election news
    sitemap_urls = ['https://www.nytimes.com/sitemaps/sitemap_news/sitemap.xml.gz']

    def parse(self, response):
        article = response.xpath('//html[@itemtype="http://schema.org/NewsArticle"]')
        if article is None:
            return

        item = NewsItem()

        item['url'] = response.xpath('//html[@itemtype="http://schema.org/NewsArticle"]/@itemid').extract_first()
        if item['url'] is None:
            return

        title = response.xpath('//html/head/title/text()').extract_first()
        if title is None:
            return

        index = title.index('- The New York Times')
        if index >= 0:
            title = title[0:index]

        item['title'] = remove_unicode(title)

        description = response.xpath('/html/head/meta[@name="description"]/@content').extract_first()
        item['description'] = remove_unicode(description)
        if item['description'] is None:
            return

        date = response.xpath('//time/@datetime').extract_first()
        if date is None:
            return

        item['date'] = parse(date).strftime("%Y-%m-%d %H:%M:%S")
        if item['date'] is None:
            return

        item['author'] = (" ".join(response.xpath('//*[@itemprop="author creator"]//text()').extract())).strip()
        if item['author'] is None:
            item['author'] = ''

        articleBody = response.xpath('//*[@id="story"]/section[@name="articleBody"]').extract_first()
        if articleBody is None:
            return

        content = " ".join(response.xpath('//*[@id="story"]/section[@name="articleBody"]//p/text()').extract())
        if content is None:
            return

        item['content'] = remove_unicode(content)

        yield item