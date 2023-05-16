import os

from atcScrapy.lib.database.write import execute_db_insert

class atc_scrapy_db_pipeline:

    def process_item(self, item, spider):

        db_keys_env_name = f"DB_{spider.name.upper()}_KEYS"
        db_keys_env = os.getenv(db_keys_env_name)

        if db_keys_env:

            network_keys = db_keys_env.split(",")

            network_values = list(item.values())

            execute_db_insert(
                query_table_name="networks",
                query_keys=network_keys,
                query_values=network_values
            )

            return item

        else:

            raise Exception(f"[ATC] The env key/value '{db_keys_env_name}' could not be found - add it.")
