import os

from atcScrapy.lib.database.write import execute_db_insert

class ATCScrapyDBPipeline:

    def process_item(self, item, spider):

        db_keys_env_name = f"DB_{spider.name.upper()}_KEYS"
        db_keys_env = os.getenv(db_keys_env_name)

        if db_keys_env:

            db_keys = db_keys_env.split(",")

            db_values = []
            for db_key in db_keys:
                item_value = item[db_key]
                db_values.append(item_value)

            execute_db_insert(
                query_table_name=spider.name,
                query_keys=db_keys,
                query_values=db_values
            )

            return item

        else:

            raise Exception(f"[ATC] The env key/value '{db_keys_env_name}' could not be found - add it.")
