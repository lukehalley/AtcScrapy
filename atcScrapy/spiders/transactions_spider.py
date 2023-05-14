import csv, os
import json
import re
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError


class TransactionSpider(scrapy.Spider):

    name = "transaction"
    custom_settings = {
        'FEEDS': { 'yield/transaction.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_api_base_url = os.environ["GT_API_BASE_URL"]

    if os.path.isfile('yield/pair.csv'):

        with open("yield/pair.csv", "r") as f:
            readFile = csv.DictReader(f)
            start_urls = [f'{os.environ["GT_API_BASE_URL"]}/{item["pair_network"]}/pools/{item["pair_address"]}/swaps?include=from_token%2Cto_token&page=1' for item in readFile]

        full_reader = csv.DictReader(open('yield/pair.csv'))
        pair_dict = [item for item in full_reader]

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.FormRequest(
                url,
                method='GET',
                callback=self.parse_httpbin,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def parse_httpbin(self, response):
        pair_index = self.start_urls.index(response.url)
        transaction_dicts = json.loads(response.body.decode("utf-8"))["data"]
        formatted_transaction_dicts = []
        for transaction_dict in transaction_dicts:
            formatted_transaction = {
                "transaction_type": transaction_dict["type"],
                "transaction_hash": transaction_dict["attributes"]["tx_hash"],
                "transaction_from_amount": transaction_dict["attributes"]["from_token_amount"],
                "transaction_to_amount": transaction_dict["attributes"]["to_token_amount"],
                "transaction_pair_address": self.pair_dict[pair_index]["pair_address"],
                "transaction_pair_network": self.pair_dict[pair_index]["pair_network"],
                "transaction_pair_dex": self.pair_dict[pair_index]["pair_dex"],
                "transaction_url": response.url,
            }
            formatted_transaction_dicts.append(formatted_transaction)

        for formatted_transaction_dict in formatted_transaction_dicts:
            yield formatted_transaction_dict

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)