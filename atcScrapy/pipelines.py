import os

from atcScrapy.lib.database.execute import execute_db_query

class MysqlDemoPipeline:

    def process_item(self, item, spider):

        if spider.name == "network":

            network_keys = os.getenv("DB_NETWORK_KEYS").split(",")

            network_values = (
                item["network_chain_id"],
                item["network_name"],
                item["network_identifier"],
                item["network_explorer_url"],
                "scan",
                "",
                "",
                item["network_geckoterminal_url"],
                item["network_native_currency_symbol"],
                item["network_native_currency_address"],
                5,
                1,
            )

            execute_db_query(
                query_table_name="networks",
                query_keys=network_keys,
                query_values=network_values
            )

            return item
