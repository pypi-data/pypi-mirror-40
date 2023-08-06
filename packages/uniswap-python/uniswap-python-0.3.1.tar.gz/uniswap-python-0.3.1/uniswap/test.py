import os
from web3 import Web3
from pprint import pprint

provider = os.environ["PROVIDER"]
w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))

pprint(w3.eth.getTransactionReceipt(0x50379b3fdb9f7ad553fef509e4e10ffeaba97471ad1736aaaa366c12242fd85b))