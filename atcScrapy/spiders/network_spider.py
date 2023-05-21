import json
import os
import re
import scrapy

from atcScrapy.items import NetworkItem


class NetworkSpider(scrapy.Spider):
    name = "network"

    lazy_mode = eval(os.environ["LAZY_MODE"])
    lazy_count = int(os.environ["LAZY_COUNT"])

    network_api_url = f'{os.environ["GT_API_BASE_URL"]}/networks'

    start_urls = [network_api_url]

    def parse(self, response, **kwargs):

        extracted_dict = json.loads(response.text)

        formatted_network_dicts = []
        for network in extracted_dict["data"]:

            if "tx/" in network["attributes"]["explorer_tx_url"]:
                explorer_url = network["attributes"]["explorer_tx_url"].split("tx/")[0]
            else:
                explorer_url = network["attributes"]["explorer_tx_url"]

            network_item = NetworkItem()

            network_item["chain_id"] = network["attributes"]["chain_id"]
            network_item["name"] = network["attributes"]["name"]
            network_item["identifier"] = network["attributes"]["identifier"]
            network_item["explorer_url"] = explorer_url
            network_item["explorer_type"] = ""
            network_item["explorer_api_prefix"] = ""
            network_item["explorer_api_key"] = ""
            network_item["native_currency_symbol"] = network["attributes"]["native_currency_symbol"]
            network_item["native_currency_address"] = network["attributes"]["native_currency_address"]
            network_item["native_currency_max_gas"] = 5
            network_item["native_currency_min_gas"] = 1

            if not None in network_item.values():
                formatted_network_dicts.append(network_item)

        if self.lazy_mode:
            formatted_network_dicts = formatted_network_dicts[0:self.lazy_count]

        for network_item in formatted_network_dicts:
            yield network_item