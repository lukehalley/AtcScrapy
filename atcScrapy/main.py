import time

from scrapy.utils.project import get_project_settings

settings = get_project_settings()

from scrapy.crawler import CrawlerProcess
from atcScrapy.spiders.rpc_spider import RPCSpider
from atcScrapy.spiders.network_spider import NetworkSpider
from atcScrapy.spiders.dex_spider import DexSpider
from atcScrapy.spiders.pair_spider import PairSpider
from atcScrapy.spiders.token_spider import TokenSpider
from atcScrapy.spiders.transactions_spider import TransactionSpider

def start_sequentially(process: CrawlerProcess, crawlers: list):
    deferred = process.crawl(crawlers[0])
    if len(crawlers) > 1:
        deferred.addCallback(lambda _: start_sequentially(process, crawlers[1:]))
    time.sleep(settings["DOWNLOAD_DELAY"])

def main():
    crawlers = [NetworkSpider, RPCSpider, DexSpider, PairSpider, TokenSpider, TransactionSpider]
    process = CrawlerProcess(settings=get_project_settings())
    start_sequentially(process, crawlers)
    process.start()

if __name__ == '__main__':
    main()