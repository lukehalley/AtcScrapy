import csv, os
import json
import re

import flatdict
import scrapy

class PairSpider(scrapy.Spider):

    name = "pair"
    custom_settings = {
        'FEEDS': { 'yield/pair.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_base_url = os.environ["GT_BASE_URL"]

    if os.path.isfile('yield/dex.csv'):
        with open("yield/dex.csv", "r") as f:
            reader = csv.DictReader(f)
            start_urls = [item['dex_url'] for item in reader]

    def parse(self, response, **kwargs):

        pair_network = response.url.replace(self.gt_base_url, "").split("/")[1]
        pair_dex = response.url.replace(self.gt_base_url, "").split("/")[2]

        reg = r'"fallback".*?}}}}}'
        extracted_json = "{" + str(re.findall(reg, response.text)[0]).replace('\\"', '')
        extracted_dict = json.loads(extracted_json)
        fallback_dict = extracted_dict["fallback"]
        first_leaf = list(fallback_dict.keys())[0]
        pair_dicts = fallback_dict[first_leaf]["data"]

        formatted_pair_dicts = []
        for pair_dict in pair_dicts:
            pool_url = f'{self.gt_base_url}/{pair_network}/pools/{pair_dict["attributes"]["address"]}'
            formatted_pair_dict = {
                "pair_name": pair_dict["attributes"]["name"].replace(" ", ""),
                "pair_network": pair_network,
                "pair_dex": pair_dex,
                "pair_pool_url": pool_url,
                "pair_address": pair_dict["attributes"]["address"]
            }
            formatted_pair_dicts.append(formatted_pair_dict)

        for formatted_pair_dict in formatted_pair_dicts:
            yield formatted_pair_dict