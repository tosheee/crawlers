import pkgutil

BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
pkgutil.get_loader('scrapy_settings.settings')
