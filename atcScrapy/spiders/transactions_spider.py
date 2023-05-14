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
            start_urls = [f'{os.environ["GT_API_BASE_URL"]}/{item["pair_network"]}/pools/{item["pair_address"]}/swaps' for item in readFile]

        full_reader = csv.DictReader(open('yield/pair.csv'))
        pair_dict = [item for item in full_reader]

    def start_requests(self):

        params = {
            'include': 'from_token,to_token',
            'page': '1',
        }

        for url in self.start_urls:
            yield scrapy.FormRequest(
                url,
                formdata=params,
                method='GET',
                callback=self.parse_httpbin,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def parse_httpbin(self, response):
        self.logger.info('Recieved response from {}'.format(response.url))
        response_json = json.loads(response.body.decode("utf-8"))
        x = 1

    def errback_httpbin(self, failure):
        # logs failures
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