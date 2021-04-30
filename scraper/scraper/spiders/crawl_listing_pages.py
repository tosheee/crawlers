# -*- coding: utf-8 -*-
import re
from scraper.items import ScraperItem
from scrapers import PagesScraper
from scraper.spiders.crawl_page import CrawlPage


class CrawlListingPages(CrawlPage, PagesScraper):
    name = 'scraper'

    def scrape_listing_pages(self, response):

        base_attributes = self.settings.get("BASE_ATTRIBUTES", {})
        item_fields = self.settings.get('ITEM_FIELDS', [])
        articles = response.css(base_attributes.get('list_articles', ''))

        for article in articles:
            item = ScraperItem()
            content = {}

            organization = response.meta.get('organization', '')
            content['organization'] = organization

            target = response.meta.get('target', '')
            content['target'] = target

            filter = response.meta.get('filter', '')
            content['filter'] = filter

            try:
                for item_field in item_fields:

                    field = item_field.get('field', '')
                    selector = item_field.get('selector', '')
                    method = item_field.get('method', '')

                    if not selector or not field:
                        continue

                    value = article.css(selector).getall()

                    if selector == 'response_url':
                        value = [response.url]

                    if value:
                        extract_value = ' '.join(value).strip() if method == 'all' else value[0]

                        if field == 'url':
                            extract_value = response.urljoin(extract_value)

                        if field == 'image' and method == 'join':
                            extract_value = response.urljoin(extract_value)

                        content[field] = extract_value

                item['content'] = content

                if self.settings.get('ONLY_LISTING_PAGES'):
                    yield item
                else:
                    yield response.follow(url=item.get('content', {}).get('url', ''),
                                          meta={'item': item},
                                          callback=self.extract_page,
                                          dont_filter=True)
            except ValueError as e:
                print('Extract broken {}'.format(e))

        next_url = response.css(base_attributes.get('next_page', '')).get()
        if next_url:
            yield response.follow(next_url,
                                  callback=self.scrape_listing_pages,
                                  meta={'organization': organization,
                                        'target': target,
                                        'filter': filter})
