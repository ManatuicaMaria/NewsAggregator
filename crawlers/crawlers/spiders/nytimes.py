from scrapy.spiders import SitemapSpider
from crawlers.items import NewsItem
from dateutil.parser import parse


class NytSpider(SitemapSpider):
    name = 'nytimes'
    allowed_domains = ['www.nytimes.com']
    # not sure if this could be used: https://spiderbites.nytimes.com/
    sitemap_urls = ['https://www.nytimes.com/sitemaps/www.nytimes.com/sitemap.xml.gz']

    def parse(self, response):
        article = response.xpath('//html[@itemtype="http://schema.org/NewsArticle"]')
        if article is None:
            return

        item = NewsItem()

        item['url'] = article.xpath('//html/@itemid').extract_first()
        if item['url'] is None:
            return

        title = response.xpath('///html/head/title/text()').extract_first()
        if title is None:
            return

        index = title.index(' - The New York Times')
        if index >= 0:
            title = title[0:index]

        item['title'] = title

        item['description'] = response.xpath('/html/head/meta[@name="description"]/@content').extract_first()
        if item['description'] is None:
            return

        item['date'] = parse(response.xpath('//time/@datetime').extract_first())
        if item['date'] is None:
            return

        item['author'] = response.xpath('//*[@itemprop="author creator"]').xpath('string()').extract_first()
        if item['author'] is None:
            return

        articleBody = response.xpath('//*[@id="story"]/section[@name="articleBody"]')
        if articleBody is None:
            return

        content = []
        paragraphs = articleBody.xpath(
            '//*[@class="css-u5vfum StoryBodyCompanionColumn"]/div/p[@class="css-1ebnwsw e2kc3sl0"]')

        if len(paragraphs) == 0:
            print('no paragraphs for ' + item['title'])
            return

        for p in paragraphs:
            content.extend(p.xpath('string()').extract())

        item['content'] = ' '.join(content)

        yield item