import json
import os
import re
import scrapy

from atcScrapy.items import NetworkItem


class NetworkSpider(scrapy.Spider):
    name = "network"
    custom_settings = {
        'FEEDS': { 'yield/network.csv': { 'format': 'csv', 'overwrite': True}}
    }

    lazy_mode = eval(os.environ["LAZY_MODE"])
    lazy_count = int(os.environ["LAZY_COUNT"])
    start_urls = [os.environ["GT_BASE_URL"]]

    def parse(self, response, **kwargs):

        reg = r'<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>'
        extracted_json = re.findall(reg, response.text)[0].replace('\\"', '')
        extracted_dict = json.loads(extracted_json)

        formatted_network_dicts = []
        for network in extracted_dict["props"]["networks"]:

            if "tx/" in network["attributes"]["explorer_tx_url"]:
                explorer_url = network["attributes"]["explorer_tx_url"].split("tx/")[0]
            else:
                explorer_url = network["attributes"]["explorer_tx_url"]

            network_geckoterminal_url = f'{self.start_urls[0]}/{network["attributes"]["identifier"]}/pools'

            network_item = NetworkItem()

            network_item["network_name"] = network["attributes"]["name"]
            network_item["network_chain_id"] = network["attributes"]["chain_id"]
            network_item["network_identifier"] = network["attributes"]["identifier"]
            network_item["network_native_currency_symbol"] = network["attributes"]["native_currency_symbol"]
            network_item["network_native_currency_address"] = network["attributes"]["native_currency_address"]
            network_item["network_explorer_url"] = explorer_url
            network_item["network_geckoterminal_url"] = network_geckoterminal_url

            if not None in network_item.values():
                formatted_network_dicts.append(network_item)

        if self.lazy_mode:
            formatted_network_dicts = formatted_network_dicts[0:self.lazy_count]

        for network_item in formatted_network_dicts:
            yield network_item