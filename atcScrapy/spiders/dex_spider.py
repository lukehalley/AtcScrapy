import csv, os
import scrapy
from scrapy.linkextractors import LinkExtractor

class DexSpider(scrapy.Spider):

    name = "dex"
    custom_settings = {
        'FEEDS': { 'yield/dex.csv': { 'format': 'csv', 'overwrite': True}}
    }
    gt_base_url = os.environ["GT_BASE_URL"]
    gt_pair_pages = int(os.environ["GT_PAIR_PAGES"])

    if os.path.isfile('yield/network.csv'):
        with open("yield/network.csv", "r") as f:
            reader = csv.DictReader(f)
            start_urls = [item['network_url'] for item in reader]

    def parse(self, response, **kwargs):

        dex_network = response.url.replace(self.gt_base_url, "").split("/")[1]
        network_url_reg_exp = rf'\/{dex_network}\/.*\/pools$'

        link_extractor = LinkExtractor(allow=network_url_reg_exp, restrict_xpaths='//a', unique=True)

        network_links = link_extractor.extract_links(response)

        for link in network_links:
            if link.text != "" and dex_network != "" and link.url != "":
                for i in range(self.gt_pair_pages):
                    if i > 0:
                        i = i + 1
                        final_link = f"{link.url}?page={i}"
                    else:
                        final_link = link.url
                    yield {"dex_name": link.text, "dex_network": dex_network, "dex_url": final_link}