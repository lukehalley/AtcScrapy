import os
import dotenv
from atcScrapy.lib.logging import QuietLogFormatter

dotenv.load_dotenv()

BOT_NAME = "atcScrapy"

SPIDER_MODULES = ["atcScrapy.spiders"]
NEWSPIDER_MODULE = "atcScrapy.spiders"

ROBOTSTXT_OBEY = False

LOG_FORMATTER = QuietLogFormatter

CONCURRENT_REQUESTS = int(os.environ["CONCURRENT_REQUESTS"])

DOWNLOAD_DELAY = int(os.environ["DOWNLOAD_DELAY"])
RANDOMIZE_DOWNLOAD_DELAY = True

DEFAULT_REQUEST_HEADERS = {
    "X-Crawlera-Profile": "mobile",
    "X-Crawlera-Cookies": "disable",
}

DOWNLOADER_MIDDLEWARES = {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610}
ZYTE_SMARTPROXY_ENABLED = False
ZYTE_SMARTPROXY_APIKEY = 'e9140330151c44a5a47b2fff69c15874'

ITEM_PIPELINES = {
   'atcScrapy.pipelines.ATCScrapyDBPipeline': 300,
}

AUTOTHROTTLE_ENABLED = True
DOWNLOAD_TIMEOUT = 600

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
