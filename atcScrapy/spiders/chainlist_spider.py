import csv, os
import json
import re
import scrapy

class ChainlistSpider(scrapy.Spider):
    name = "chainlist"
    custom_settings = {
        'FEEDS': {'yield/rpcs.csv': {'format': 'csv', 'overwrite': True}}
    }

    cl_base_url = os.environ["CL_BASE_URL"]

    if os.path.isfile('yield/network.csv'):
        with open("yield/network.csv", "r") as f:
            readFile = csv.DictReader(f)
            start_urls = [f'{os.environ["CL_BASE_URL"]}/{item["network_chain_id"]}' for item in readFile]

        full_reader = csv.DictReader(open('yield/network.csv'))
        network_dict = [item for item in full_reader]

    def parse(self, response, **kwargs):

        network_index = self.start_urls.index(response.url)

        reg = r'<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>'
        extracted_json = re.findall(reg, response.text)[0].replace('\\"', '')
        extracted_dict = json.loads(extracted_json)

        filtered_rpc_urls = [network_rpc["url"] for network_rpc in extracted_dict["props"]["pageProps"]["chain"]["rpc"] if "API_KEY" not in network_rpc["url"]]
        joined_rpc_urls = ",".join(filtered_rpc_urls)

        chainlist_data_dict = {
                "rpc_network_id": self.network_dict[network_index]["network_chain_id"],
                "rpc_url": joined_rpc_urls
        }

        all_values_present = bool(chainlist_data_dict) and all(chainlist_data_dict.values())

        if all_values_present:
            yield chainlist_data_dict