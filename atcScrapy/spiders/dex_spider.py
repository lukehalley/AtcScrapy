import json
import os

import scrapy

from atcScrapy.items import DexItem
from atcScrapy.lib.database.read import execute_db_query


class DexSpider(scrapy.Spider):
    name = "dex"

    lazy_mode = eval(os.environ["LAZY_MODE"])
    lazy_count = int(os.environ["LAZY_COUNT"])

    gt_base_url = os.environ["GT_OFFICIAL_BASE_URL"]

    networks_db = execute_db_query(
        query="SELECT * FROM network"
    )

    start_urls = [f'{os.environ["GT_OFFICIAL_BASE_URL"]}/networks/{network_db["identifier"]}/dexes' for network_db in networks_db]

    def parse(self, response, **kwargs):

        network_index = self.start_urls.index(response.url)

        dex_network = self.networks_db[network_index]
        dex_network_chain_id = dex_network["chain_id"]

        extracted_dict = json.loads(response.text)

        for dex in extracted_dict["data"]:
            dex_item = DexItem()
            dex_item["chain_id"] = dex_network_chain_id
            dex_item["name"] = dex["attributes"]["name"]
            dex_item["identifier"] = dex["id"]
            dex_item["router_address"] = ""
            dex_item["factory_address"] = ""
            yield dex_item
