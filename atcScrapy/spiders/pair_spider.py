import json
import os
import re

import scrapy

from atcScrapy.items import PairItem
from atcScrapy.lib.database.read import execute_db_query


class PairSpider(scrapy.Spider):

    name = "pair"
    custom_settings = {
        'FEEDS': { 'yield/pair.csv': { 'format': 'csv', 'overwrite': True}}
    }

    gt_base_url = os.environ["GT_BASE_URL"]
    gt_pair_pages = int(os.environ["GT_PAIR_PAGES"])

    networks_and_dexs_db = execute_db_query(
        query="SELECT "
              "network.chain_id, "
              "dex.dex_id, "
              "network.identifier AS network_identifier, "
              "dex.identifier AS dex_identifier "
              "FROM dex "
              "INNER JOIN network "
              "ON dex.chain_id = network.chain_id"
    )

    # https://app.geckoterminal.com/api/p1/eth/pools?dex=uniswap_v3&include=dex,dex.dex_metric,dex.network,tokens&page=1&include_network_metrics=true
    start_urls = [f'{os.environ["GT_API_BASE_URL"]}/{network_and_dex_db["network_identifier"]}/pools?dex={network_and_dex_db["dex_identifier"]}&include=dex,dex.dex_metric,dex.network,tokens&page=1&include_network_metrics=true' for network_and_dex_db in networks_and_dexs_db]

    def parse(self, response, **kwargs):

        network_dex_index = self.start_urls.index(response.url)

        pair_network_dex = self.networks_and_dexs_db[network_dex_index]
        pair_chain_id = pair_network_dex["chain_id"]
        pair_network_identifier = pair_network_dex["network_identifier"]
        pair_dex_id = pair_network_dex["dex_id"]

        extracted_dict = json.loads(response.text)

        pair_items = []
        for pair_dict in extracted_dict["data"]:

            pair_item = PairItem()

            pair_name_split = pair_dict["attributes"]["name"].split(" ")

            if len(pair_name_split) >= 3:

                primary_token_name = pair_name_split[0]
                quote_token_name = pair_name_split[2]
                pair_name = f'{primary_token_name}/{quote_token_name}'

                pair_item["primary_token_id"] = None
                pair_item["quote_token_id"] = None
                pair_item["chain_id"] = pair_chain_id
                pair_item["dex_id"] = pair_dex_id
                pair_item["name"] = pair_name
                pair_item["primary_token_name"] = primary_token_name
                pair_item["quote_token_name"] = quote_token_name
                pair_item["address"] = pair_dict["attributes"]["address"]

                pair_items.append(pair_item)

        for pair_item in pair_items:
            yield pair_item