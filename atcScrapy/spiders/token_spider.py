import csv, os
import json
import re
import scrapy

from atcScrapy.items import TokenItem
from atcScrapy.lib.database.read import execute_db_query
from atcScrapy.lib.database.write import execute_db_update


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
        pair = self.networks_and_pairs_db[pair_index]

        reg = r'<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>'
        extracted_json = re.findall(reg, response.text)[0].replace('\\"', '')
        extracted_dict = json.loads(extracted_json)

        # Extract the primary token

        primary_token_item = TokenItem()

        primary_token = extracted_dict["props"]["pageProps"]["data"]["token"]["byId"][list(extracted_dict["props"]["pageProps"]["data"]["token"]["byId"].keys())[-1]]
        primary_token_item["name"] = primary_token["attributes"]["name"]
        primary_token_item["symbol"] = primary_token["attributes"]["symbol"]
        primary_token_item["address"] = primary_token["attributes"]["address"]
        primary_token_item["decimals"] = primary_token["attributes"]["decimals"]

        # Extract the quote token

        quote_token_item = TokenItem()

        quote_token = extracted_dict["props"]["pageProps"]["data"]["token"]["byId"][list(extracted_dict["props"]["pageProps"]["data"]["token"]["byId"].keys())[0]]
        quote_token_item["name"] = quote_token["attributes"]["name"]
        quote_token_item["symbol"] = quote_token["attributes"]["symbol"]
        quote_token_item["address"] = quote_token["attributes"]["address"]
        quote_token_item["decimals"] = quote_token["attributes"]["decimals"]

        # Add comment info

        primary_token_item["chain_id"] = quote_token_item["chain_id"] = pair["chain_id"]
        primary_token_item["dex_id"] = quote_token_item["dex_id"] = pair["dex_id"]
        primary_token_item["pair_id"] = quote_token_item["pair_id"] = pair["pair_id"]

        yield primary_token_item

        primary_token_id = execute_db_query(
            query='SELECT token.token_id '
                  'FROM token '
                  'WHERE '
                  f'token.chain_id = {primary_token_item["chain_id"]} '
                  'AND '
                  f'token.dex_id = {primary_token_item["dex_id"]} '
                  'AND '
                  f'token.pair_id = {primary_token_item["pair_id"]} '
                  'AND '
                  f'token.address = "{primary_token_item["address"]}"'
        )[0]["token_id"]

        yield quote_token_item

        quote_token_id = execute_db_query(
            query='SELECT token.token_id '
                  'FROM token '
                  'WHERE '
                  f'token.chain_id = {quote_token_item["chain_id"]} '
                  'AND '
                  f'token.dex_id = {quote_token_item["dex_id"]} '
                  'AND '
                  f'token.pair_id = {quote_token_item["pair_id"]} '
                  'AND '
                  f'token.address = "{quote_token_item["address"]}"'
        )[0]["token_id"]

        # Update Pair with token ids
        execute_db_update(
            query_table_name="pair",
            update_dict={
                "primary_token_id": primary_token_id,
                "quote_token_id": quote_token_id
            },
            where_dict={
                "pair.pair_id": primary_token_item["pair_id"],
                "pair.chain_id": quote_token_item["chain_id"]
            }

        )