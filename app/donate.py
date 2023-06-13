from flask import request
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545')) # network

def transaction(user, address_to, value):
    print(f'Attempting to send transaction from {user.username} to {address_to}')
    # set the gas price strategy
    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(
        {
            'nonce': web3.eth.get_transaction_count(user.ganache_address),
            'gasPrice': web3.eth.generate_gas_price(),
            'gas': 21000,
            'to': address_to,
            'value': web3.to_wei(str(value), 'ether'),
        },
        user.pk
    )
    # Send rx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Transaction successful with hash: {tx_receipt.transactionHash.hex()}')