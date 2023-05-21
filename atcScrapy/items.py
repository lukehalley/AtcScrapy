import scrapy
from scrapy import Field

class NetworkItem(scrapy.Item):
    chain_id = Field()
    name = Field()
    identifier = Field()
    explorer_url = Field()
    explorer_type = Field()
    explorer_api_prefix = Field()
    explorer_api_key = Field()
    geckoterminal_url = Field()
    native_currency_symbol = Field()
    native_currency_address = Field()
    native_currency_max_gas = Field()
    native_currency_min_gas = Field()

class DexItem(scrapy.Item):
    dex_id = Field()
    chain_id = Field()
    name = Field()
    identifier = Field()
    router_address = Field()
    factory_address = Field()

class RPCItem(scrapy.Item):
    rpc_id = Field()
    chain_id = Field()
    url = Field()

class PairItem(scrapy.Item):
    primary_token_id = Field()
    quote_token_id = Field()
    chain_id = Field()
    dex_id = Field()
    name = Field()
    primary_token_name = Field()
    quote_token_name = Field()
    address = Field()

class TokenItem(scrapy.Item):
    chain_id = Field()
    name = Field()
    symbol = Field()
    decimals = Field()
    address = Field()