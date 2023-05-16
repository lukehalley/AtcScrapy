import scrapy
from scrapy import Field

class NetworkItem(scrapy.Item):
    network_name = Field()
    network_chain_id = Field()
    network_identifier = Field()
    network_native_currency_symbol = Field()
    network_native_currency_address = Field()
    network_explorer_url = Field()
    network_geckoterminal_url = Field()
