import scrapy
from scrapy.linkextractors import LinkExtractor

class NetworkSpider(scrapy.Spider):
    name = "network"
    custom_settings = {
        'FEEDS': { 'yield/network.csv': { 'format': 'csv', 'overwrite': True}}
    }

    start_urls = ["https://www.geckoterminal.com/"]

    def parse(self, response, **kwargs):

        network_url_reg_exp = r'.*/pools$'

        link_extractor = LinkExtractor(allow=network_url_reg_exp, restrict_xpaths='//a', unique=True)

        network_links = link_extractor.extract_links(response)

        for link in network_links:
            yield {"url": link.url, "text": link.text}