import json
import os
import re

import scrapy

from atcScrapy.items import RPCItem, ExplorerItem
from atcScrapy.lib.database.read import execute_db_query


class RPCSpider(scrapy.Spider):
    name = "rpc"

    chainlist_base_url = os.environ["CL_BASE_URL"]

    networks_db = execute_db_query(
        query="SELECT * FROM network"
    )

    start_urls = [f'{os.environ["CL_BASE_URL"]}/{network_db["chain_id"]}' for network_db in networks_db]

    def parse(self, response, **kwargs):

        network_index = self.start_urls.index(response.url)

        rpc_network = self.networks_db[network_index]
        rpc_network_chain_id = rpc_network["chain_id"]

        reg = r'<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>'
        extracted_json = re.findall(reg, response.text)[0].replace('\\"', '')
        extracted_dict = json.loads(extracted_json)

        chain_data = extracted_dict["props"]["pageProps"]["chain"]

        if "rpc" in chain_data:

            filtered_rpc_urls = [network_rpc["url"] for network_rpc in chain_data["rpc"] if "API_KEY" not in network_rpc["url"]]

            for filtered_rpc_url in filtered_rpc_urls:
                rpc_item = RPCItem()
                rpc_item["chain_id"] = rpc_network_chain_id
                rpc_item["url"] = filtered_rpc_url
                yield rpc_item

        if "explorers" in chain_data:

            network_explorers = [network_explorer for network_explorer in chain_data["explorers"]]

            for network_explorer in network_explorers:
                explorer_item = ExplorerItem()
                explorer_item["chain_id"] = rpc_network_chain_id
                explorer_item["name"] = network_explorer["name"]
                explorer_item["url"] = network_explorer["url"]
                explorer_item["standard"] = network_explorer["standard"]
                yield explorer_item