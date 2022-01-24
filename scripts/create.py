from brownie import advnft, config

from scripts.help import get_account
from scripts.help import fund_with_link, get_account, get_contract, local_env
from web3 import Web3


def create_function():
    account = get_account()
    nft = advnft[-1]
    tx = fund_with_link(nft.address, amount=Web3.toWei(0.1, "ether"))
    tx.wait(1)
    create_tx = nft.create("dog", {"from": account})
    create_tx.wait(1)


def main():
    create_function()
