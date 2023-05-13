import csv
import os

import scrapy
from scrapy.linkextractors import LinkExtractor

class DexSpider(scrapy.Spider):

    name = "dex"
    custom_settings = {
        'FEEDS': { 'yield/dex.csv': { 'format': 'csv', 'overwrite': True}}
    }

    if os.path.isfile('yield/network.csv'):
        with open("yield/network.csv", "r") as f:
            reader = csv.DictReader(f)
            start_urls = [item['url'] for item in reader]
    else:
        raise Exception("'yield/network.csv' could not be found, run Network spiders first.")

    def parse(self, response, **kwargs):

        network_url_reg_exp = r'.*/pools$'

        link_extractor = LinkExtractor(allow=network_url_reg_exp, restrict_xpaths='//a', unique=True)

        network_links = link_extractor.extract_links(response)

        for link in network_links:
            yield {"url": link.url, "text": link.text}