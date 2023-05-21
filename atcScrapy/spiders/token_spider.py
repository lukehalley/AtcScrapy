import csv, os
import json
import re
import scrapy

from atcScrapy.lib.database.read import execute_db_query


class TokenSpider(scrapy.Spider):

    name = "token"
    custom_settings = {
        'FEEDS': { 'yield/token.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_base_url = os.environ["GT_BASE_URL"]

    networks_and_pairs_db = execute_db_query(
        query="SELECT "
              "pair.pair_id pair_id, "
              "pair.name pair_name, "
              "pair.address pair_address, "
              "network.chain_id, "
              "network.identifier network_identifier, "
              "dex.dex_id, "
              "dex.identifier dex_identifier "
              "FROM dex "
              "INNER JOIN network ON dex.chain_id = network.chain_id "
              "INNER JOIN pair ON dex.dex_id = pair.dex_id"
    )

    start_urls = [f'{os.environ["GT_BASE_URL"]}/{network_and_pair_db["network_identifier"]}/pools/{network_and_pair_db["pair_address"]}' for network_and_pair_db in networks_and_pairs_db]


    def parse(self, response, **kwargs):

        pair_index = self.start_urls.index(response.url)

        reg = r'<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>'
        extracted_json = re.findall(reg, response.text)[0].replace('\\"', '')
        extracted_dict = json.loads(extracted_json)

        primary_quote_dict = {}

        primary_token = extracted_dict["props"]["pageProps"]["data"]["token"]["byId"][list(extracted_dict["props"]["pageProps"]["data"]["token"]["byId"].keys())[-1]]
        primary_quote_dict["primary_token_name"] = primary_token["attributes"]["name"]
        primary_quote_dict["primary_token_symbol"] = primary_token["attributes"]["symbol"]
        primary_quote_dict["primary_token_address"] = primary_token["attributes"]["address"]
        primary_quote_dict["primary_token_decimals"] = primary_token["attributes"]["decimals"]
        
        quote_token = extracted_dict["props"]["pageProps"]["data"]["token"]["byId"][list(extracted_dict["props"]["pageProps"]["data"]["token"]["byId"].keys())[0]]
        primary_quote_dict["quote_token_name"] = quote_token["attributes"]["name"]
        primary_quote_dict["quote_token_symbol"] = quote_token["attributes"]["symbol"]
        primary_quote_dict["quote_token_address"] = quote_token["attributes"]["address"]
        primary_quote_dict["quote_token_decimals"] = quote_token["attributes"]["decimals"]

        pairs_dict_merged = primary_quote_dict | self.networks_and_pairs_db[pair_index]

        yield pairs_dict_merged