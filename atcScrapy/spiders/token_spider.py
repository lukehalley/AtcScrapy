import csv, os
import json
import re
import scrapy

class TokenSpider(scrapy.Spider):

    name = "token"
    custom_settings = {
        'FEEDS': { 'yield/token.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_base_url = os.environ["GT_BASE_URL"]

    if os.path.isfile('yield/pair.csv'):

        with open("yield/pair.csv", "r") as f:
            readFile = csv.DictReader(f)
            start_urls = [item['pair_pool_url'] for item in readFile]

        full_reader = csv.DictReader(open('yield/pair.csv'))
        pair_dict = [item for item in full_reader]

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

        pairs_dict_merged = primary_quote_dict | self.pair_dict[pair_index]

        yield pairs_dict_merged