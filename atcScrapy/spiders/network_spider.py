import json
import os
import re
import scrapy

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
                explorer_tx_url = network["attributes"]["explorer_tx_url"].split("tx/")[0] + "tx/"
            else:
                explorer_tx_url = network["attributes"]["explorer_tx_url"] + "/tx/"

            network_url = f'{self.start_urls[0]}/{network["attributes"]["identifier"]}/pools'

            formatted_network_dict = {
                "network_name": network["attributes"]["name"],
                "network_chain_id": network["attributes"]["chain_id"],
                "network_identifier": network["attributes"]["identifier"],
                "network_native_currency_symbol": network["attributes"]["native_currency_symbol"],
                "network_native_currency_address": network["attributes"]["native_currency_address"],
                "network_explorer_tx_url": explorer_tx_url,
                "network_url": network_url
            }

            all_values_present = bool(formatted_network_dict) and all(formatted_network_dict.values())

            if all_values_present:
                formatted_network_dicts.append(formatted_network_dict)

        if self.lazy_mode:
            formatted_network_dicts = formatted_network_dicts[0:self.lazy_count]

        for formatted_network_dict in formatted_network_dicts:
            yield formatted_network_dict