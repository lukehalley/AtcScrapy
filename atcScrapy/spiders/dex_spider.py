import csv, os
import scrapy
from scrapy.linkextractors import LinkExtractor

from atcScrapy.items import DexItem
from atcScrapy.lib.database.read import execute_db_query


class DexSpider(scrapy.Spider):

    name = "dex"
    custom_settings = {
        'FEEDS': { 'yield/dex.csv': { 'format': 'csv', 'overwrite': True}}
    }

    lazy_mode = eval(os.environ["LAZY_MODE"])
    lazy_count = int(os.environ["LAZY_COUNT"])

    gt_base_url = os.environ["GT_BASE_URL"]
    gt_pair_pages = int(os.environ["GT_PAIR_PAGES"])

    networks_db = execute_db_query(
        query="SELECT * FROM networks"
    )

    start_urls = [network_db['geckoterminal_url'] for network_db in networks_db]

    def parse(self, response, **kwargs):

        dex_network = response.url.replace(self.gt_base_url, "").split("/")[1]
        network_url_reg_exp = rf'\/{dex_network}\/.*\/pools$'

        link_extractor = LinkExtractor(allow=network_url_reg_exp, restrict_xpaths='//a', unique=True)

        network_links = link_extractor.extract_links(response)

        if self.lazy_mode:
            network_links = network_links[0:self.lazy_count]

        for link in network_links:
            if link.text != "" and dex_network != "" and link.url != "":
                for i in range(self.gt_pair_pages):
                    if i > 0:
                        i = i + 1
                        final_link = f"{link.url}?page={i}"
                    else:
                        final_link = link.url
                    dex_item = DexItem()
                    dex_item["dex_name"] = link.text
                    dex_item["dex_network"] = dex_network
                    dex_item["dex_url"] = final_link
                    yield dex_item