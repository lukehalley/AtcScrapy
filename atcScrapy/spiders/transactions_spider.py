import os
import json
import scrapy
from atcScrapy.items import TokenItem, TransactionItem
from atcScrapy.lib.database.read import execute_db_query
from atcScrapy.lib.database.write import execute_db_update


class TransactionSpider(scrapy.Spider):

    name = "transaction"
    custom_settings = {
        'FEEDS': { 'yield/transaction.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_api_base_url = os.environ["GT_API_BASE_URL"]

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

    start_urls = [f'{os.environ["GT_API_BASE_URL"]}/{network_and_pair_db["network_identifier"]}/pools/{network_and_pair_db["pair_address"]}/swaps?include=from_token,to_token&page=1' for network_and_pair_db in networks_and_pairs_db]


    def parse(self, response, **kwargs):

        network_pair_index = self.start_urls.index(response.url)

        network_pair_index = self.networks_and_pairs_db[network_pair_index]
        pair_id = network_pair_index["pair_id"]
        pair_chain_id = network_pair_index["chain_id"]
        pair_dex_id = network_pair_index["dex_id"]

        extracted_dict = json.loads(response.text)

        primary_token_item = TokenItem()

        primary_token = extracted_dict["included"][0]
        primary_token_item["name"] = primary_token["attributes"]["name"]
        primary_token_item["symbol"] = primary_token["attributes"]["symbol"]
        primary_token_item["address"] = primary_token["attributes"]["address"]
        primary_token_item["decimals"] = None
        primary_token_item["chain_id"] = pair_chain_id
        primary_token_item["dex_id"] = pair_dex_id
        primary_token_item["pair_id"] = pair_id

        yield primary_token_item

        primary_token_id = execute_db_query(
            query='SELECT token.token_id '
                  'FROM token '
                  'WHERE '
                  f'token.chain_id = {pair_chain_id} '
                  'AND '
                  f'token.dex_id = {pair_dex_id} '
                  'AND '
                  f'token.pair_id = {pair_id} '
                  'AND '
                  f'token.address = "{primary_token_item["address"]}"'
        )[0]["token_id"]

        quote_token_item = TokenItem()

        quote_token = extracted_dict["included"][-1]
        quote_token_item["name"] = quote_token["attributes"]["name"]
        quote_token_item["symbol"] = quote_token["attributes"]["symbol"]
        quote_token_item["address"] = quote_token["attributes"]["address"]
        quote_token_item["decimals"] = None
        quote_token_item["chain_id"] = pair_chain_id
        quote_token_item["dex_id"] = pair_dex_id
        quote_token_item["pair_id"] = pair_id

        yield quote_token_item

        quote_token_id = execute_db_query(
            query='SELECT token.token_id '
                  'FROM token '
                  'WHERE '
                  f'token.chain_id = {pair_chain_id} '
                  'AND '
                  f'token.dex_id = {pair_dex_id} '
                  'AND '
                  f'token.pair_id = {pair_id} '
                  'AND '
                  f'token.address = "{quote_token_item["address"]}"'
        )[0]["token_id"]

        execute_db_update(
            query_table_name="pair",
            update_dict={
                "primary_token_id": primary_token_id,
                "quote_token_id": quote_token_id
            },
            where_dict={
                "pair.pair_id": pair_id,
                "pair.chain_id": pair_chain_id
            }

        )

        for tx in extracted_dict["data"]:

            tx_item = TransactionItem()
            tx_item["chain_id"] = pair_chain_id
            tx_item["dex_id"] = pair_dex_id
            tx_item["pair_id"] = pair_id
            tx_item["type"] = tx["type"]
            tx_item["hash"] = tx["attributes"]["tx_hash"]
            tx_item["to_amount"] = tx["attributes"]["to_token_amount"]
            tx_item["from_amount"] = tx["attributes"]["from_token_amount"]

            yield tx_item