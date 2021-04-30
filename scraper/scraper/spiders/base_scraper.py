# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pymysql
from scraper.items import ScraperItem
from scrapers import PagesScraper



class BaseScraper(PagesScraper):
    # name = 'scraper'

    def scrape_listing_pages(self, response):
        # import pdb; pdb.set_trace()

        for article in response.css('.realty-block__wrapper .realty-preview'):
            item = ScraperItem()

            sub_title = article.css('.realty-content-layout__sub-title-row span::text').get()
            pattern = r'град Пазарджик|гр\. Пазарджик, Център'

            if not re.search(pattern, sub_title):
                continue
             # да се тества лодъра в един json

            item['article_id'] = article.css('article::attr(id)').get()
            item['title'] = article.css('.realty-preview__title-link ::text').get()
            item['url'] = response.urljoin(article.css('.realty-preview__title-link::attr(href)').get())
            item['list_url'] = response.url
            item['description'] = article.css('.realty-preview__description::text').get()
            item['price'] = re.sub(r'\s+', '', article.css('.realty-preview__price::text').get())
            item['sub_title'] = sub_title
            item['origin_site'] = article.css('.realty-preview__origin-site::text').get()
            item['info_time'] = ' '.join(article.css('.realty-preview__info.realty-preview__info--time ::text').getall())

            yield item

            # yield scrapy.Request(url=url, meta={}, callback=self.parse_author, dont_filter=True)

        next_url = response.css('a.paging-nav--right.paging-button.paging-nav::attr(href)').get()
        if next_url:
            yield response.follow(next_url,
                                  callback=self.scrape_listing_pages)


    '''
     
    ---------------------
        # if self.page<10:
        #     self.page += 1
        #     yield scrapy.Request(url=self.first_url.format(self.page), callback=self.parse)

    def parse_author(self, response):
        item = ScraperItem()

        item['quote'] = response.meta['quote']
        item['author'] = response.meta['author']
        item['tags'] = response.meta['tags']
        item['url'] = response.meta['url']
        item['born_date'] = response.xpath('//span[@class="author-born-date"]/text()').extract()[0]
        item['born_location'] = response.xpath('//span[@class="author-born-location"]/text()').extract()[0][3:]

        item['description'] = response.xpath('//div[@class="author-description"]/text()').extract()[0].strip()

        yield item
'''