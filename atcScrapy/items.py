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
    router_address = Field()
    factory_address = Field()
    geckoterminal_url = Field()