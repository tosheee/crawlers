import pkgutil

BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
settings = pkgutil.get_loader('scrapy_settings.settings')
exec(compile(open(settings.get_filename(), "rb").read(), settings.get_filename(), 'exec'))