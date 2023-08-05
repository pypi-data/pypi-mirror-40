import os
import json
import time

from web3 import Web3


class UniswapWrapper():
    def __init__(self):
        # Initialize web3
        self.eth_address = os.environ['ETH_ADDRESS']
        self.password = os.environ['ETH_ADDRESS_PW']

        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545",
                                         request_kwargs={'timeout':60}))
        self.w3.personal.unlockAccount(self.eth_address, self.password)

        # Initialize address and contract
        path = './uniswap/'
        with open(os.path.abspath(path + 'contract_addresses.JSON')) as f:
            contract_addresses = json.load(f)
        with open(os.path.abspath(path + 'token_addresses.JSON')) as f:
            token_addressess = json.load(f)
        with open(os.path.abspath(path + 'uniswap_exchange.abi')) as f:
            exchange_abi = json.load(f)

        # Defined addresses and contract instance for each token
        self.address = {}
        self.contract = {}
        for token in contract_addresses:
            address = contract_addresses[token]
            self.address[token] = address
            self.contract[token] = self.w3.eth.contract(address=address,
                                                        abi=exchange_abi)

    # ------ Exchange ---------------------------------------------------------
    def get_fee_maker(self):
        """Get the maker fee."""
        return 0

    def get_fee_taker(self):
        """Get the maker fee."""
        return 0.003

    # ------ Market -----------------------------------------------------------
    def get_eth_token_input_price(self, token, qty):
        """Public price for ETH to Token trades with an exact input."""
        return self.contract[token].call().getEthToTokenInputPrice(qty)

    def get_token_eth_input_price(self, token, qty):
        """Public price for token to ETH trades with an exact input."""
        return self.contract[token].call().getTokenToEthInputPrice(qty)

    def get_eth_token_output_price(self, token, qty):
        """Public price for ETH to Token trades with an exact output."""
        return self.contract[token].call().getEthToTokenOutputPrice(qty)

    def get_token_eth_output_price(self, token, qty):
        """Public price for token to ETH trades with an exact output."""
        return self.contract[token].call().getTokenToEthOutputPrice(qty)

    # ------ Trades -----------------------------------------------------------
    def make_trade(self, in_token: str, out_token: str, qty: int) -> None:
        """Make a trade."""
        # Define token addresses
        out_token_addr = self.tokens[out_token]
        in_contract_addr = self.address[in_token]
        out_contract_addr = self.address[out_token]

        # Approve token tx
        if in_token != 'eth':
            if not self.is_approved(in_token, in_contract_addr):
                self.approve_exchange(in_token, in_contract_addr)
        if out_token != 'eth':
            if not self.is_approved(out_token, out_contract_addr):
                self.approve_exchange(out_token, out_contract_addr)

        # Define params
        deadline = int(time.time()) + 1000
        min_eth = 1
        min_tokens = 1
        tx_params = {'from': self.eth_address}

        # Chose which function to call based on tokens
        if in_token == 'eth':
            token_funcs = self.contract[out_token].functions
            func_params = [qty, deadline]
            tx_params['value'] = qty
            function = token_funcs.ethToTokenSwapInput(*func_params)
            function.transact(tx_params)
        else:
            token_funcs = self.contract[in_token].functions
            if out_token == 'eth':
                func_params = [qty, min_eth, deadline]
                function = token_funcs.tokenToEthSwapInput(*func_params)
                function.transact(tx_params)
            else:
                func_params = [qty, min_tokens, min_eth,
                               deadline, out_token_addr]
                function = token_funcs.tokenToTokenSwapInput(*func_params)
                function.transact(tx_params)


if __name__ == '__main__':
    us = UniswapWrapper()
    token = 'bat'
    out_token = 'eth'
    one_eth = 1*10**18
    qty = 1 * one_eth
    res = us.get_eth_token_input_price(token, qty)
    print(res)
    res = us.get_token_eth_input_price(token, qty)
    print(res)
    res = us.get_eth_token_output_price(token, qty)
    print(res)
    res = us.get_token_eth_output_price(token, qty)
    print(res)
