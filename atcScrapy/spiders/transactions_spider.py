import csv, os
import json
import re
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from atcScrapy.items import TokenItem
from atcScrapy.lib.database.read import execute_db_query


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

    # https://app.geckoterminal.com/api/p1/optimism/pools/0xf1f199342687a7d78bcc16fce79fa2665ef870e1/swaps?include=from_token,to_token&page=1
    start_urls = [f'{os.environ["GT_API_BASE_URL"]}/{network_and_pair_db["network_identifier"]}/pools/{network_and_pair_db["pair_address"]}/swaps?include=from_token,to_token&page=1' for network_and_pair_db in networks_and_pairs_db]


    def parse(self, response, **kwargs):

        extracted_dict = json.loads(response.text)

        primary_token_item = TokenItem()

        primary_token = extracted_dict["included"][0]
        primary_token_item["name"] = primary_token["attributes"]["name"]
        primary_token_item["symbol"] = primary_token["attributes"]["symbol"]
        primary_token_item["address"] = primary_token["attributes"]["address"]
        primary_token_item["decimals"] = None

        quote_token_item = TokenItem()

        quote_token = extracted_dict["included"][-1]
        quote_token_item["name"] = quote_token["attributes"]["name"]
        quote_token_item["symbol"] = quote_token["attributes"]["symbol"]
        quote_token_item["address"] = quote_token["attributes"]["address"]
        quote_token_item["decimals"] = None

        x = 1

    # def start_requests(self):
    #
    #     for url in self.start_urls:
    #         yield scrapy.FormRequest(
    #             url,
    #             method='GET',
    #             callback=self.parse_httpbin,
    #             errback=self.errback_httpbin,
    #             dont_filter=True
    #         )
    #
    # def parse_httpbin(self, response):
    #     pair_index = self.start_urls.index(response.url)
    #     transaction_dicts = json.loads(response.body.decode("utf-8"))["data"]
    #     formatted_transaction_dicts = []
    #     for transaction_dict in transaction_dicts:
    #         formatted_transaction = {
    #             "transaction_type": transaction_dict["type"],
    #             "transaction_hash": transaction_dict["attributes"]["tx_hash"],
    #             "transaction_from_amount": transaction_dict["attributes"]["from_token_amount"],
    #             "transaction_to_amount": transaction_dict["attributes"]["to_token_amount"],
    #             "transaction_pair_address": self.pair_dict[pair_index]["pair_address"],
    #             "transaction_pair_network": self.pair_dict[pair_index]["pair_network"],
    #             "transaction_pair_dex": self.pair_dict[pair_index]["pair_dex"],
    #             "transaction_url": response.url,
    #         }
    #         formatted_transaction_dicts.append(formatted_transaction)
    #
    #     for formatted_transaction_dict in formatted_transaction_dicts:
    #         yield formatted_transaction_dict
    #
    # def errback_httpbin(self, failure):
    #     self.logger.error(repr(failure))
    #
    #     if failure.check(HttpError):
    #         response = failure.value.response
    #         self.logger.error("HttpError occurred on %s", response.url)
    #
    #     elif failure.check(DNSLookupError):
    #         request = failure.request
    #         self.logger.error("DNSLookupError occurred on %s", request.url)
    #
    #     elif failure.check(TimeoutError, TCPTimedOutError):
    #         request = failure.request
    #         self.logger.error("TimeoutError occurred on %s", request.url)