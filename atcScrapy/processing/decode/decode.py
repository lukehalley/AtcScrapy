import csv
import os

from web3 import Web3

from atcScrapy.lib.decode.decode_api import APIDecode
from atcScrapy.lib.decode.decode_db import DBDecode
from atcScrapy.lib.decode.decode_filter import decode_filter


def decode_transactions():

    if os.path.isfile('yield/transaction.csv'):
        with open("yield/transaction.csv", "r") as f:
            reader = csv.DictReader(f)
            transactions = [item for item in reader]
    else:
        raise Exception("yield/transaction.csv not present - generate.")

    for transaction in transactions:

        # Collect Args
        RPCUrl = "https://eth.llamarpc.com"
        TxHash = transaction["transaction_hash"]

        # Connect To RPC
        web3Instance = Web3(Web3.HTTPProvider(RPCUrl))

        # Get Transaction
        TransactionDetails = web3Instance.eth.get_transaction(TxHash)

        # Decode With DB
        DecodeSuccessful, DecodeMsg, DecodeResults = DBDecode(TransactionDetails["input"])

        if not DecodeSuccessful:
            # Try Decode With API
            DecodeSuccessful, DecodeMsg, DecodeResults = APIDecode(TransactionDetails["input"])

        ResultsPresentAfterFilter, FilteredDecodeResults = decode_filter(DecodeResults)

        if not ResultsPresentAfterFilter:
            DecodeMsg = "Transactions Decoded - But None Were Swaps."

