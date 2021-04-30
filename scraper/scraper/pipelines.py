# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from datetime import datetime


class ScraperPipeline:
    def __init__(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
        path = f'tmp/scraper_{timestamp}.json'
        self.file = open(path, 'wb')

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False, indent=4) + ','

        self.file.write(data.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()
