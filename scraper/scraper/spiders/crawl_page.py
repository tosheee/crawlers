# -*- coding: utf-8 -*-
from scraper.items import ScraperItem


class CrawlPage:

    def extract_page(self, response):
        item_content = response.meta.get('item')
        item_fields_page = self.settings.get('ITEM_FIELDS_PAGE', [])
        item = ScraperItem()

        for item_field in item_fields_page:

            field = item_field.get('field', '')
            selector = item_field.get('selector', '')
            method = item_field.get('method', '')

            if not selector or not field:
                continue

            extract_value = response.css(selector).getall()

            if method == 'joinlink':
                extract_value = self.extract_links(response, extract_value)
            elif method == 'joinlink':
                extract_value = ' '.join(extract_value)
            else:
                extract_value[0]

            item_content['content'][field] = extract_value

        item = item_content
        yield item

    def extract_links(self, response, links):
        urls = []
        for link in links:
            urls.append(response.urljoin(link))

        return urls
