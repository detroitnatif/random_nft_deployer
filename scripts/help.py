from brownie import (
    accounts,
    config,
    network,
    VRFCoordinatorMock,
    MockV3Aggregator,
    LinkToken,
    MockOracle,
    interface,
    Contract,
)
from brownie.network import account
from web3 import Web3

local_env = ["development", "ganache-local", "mainnet-fork"]
contract_to_mock = {
    "link": LinkToken,
    "MockV3": MockV3Aggregator,
    "vrf": VRFCoordinatorMock,
    "oracle": MockOracle,
}


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in local_env:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    account = get_account()
    contract_type = contract_to_mock[contract_name]
    if network.show_active() not in local_env:
        contract_addy = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_addy, contract_type.abi
        )
    else:
        if len(contract_type) < 1:
            deploy_mocks()
        contract = contract_type[-1]
    return contract


def deploy_mocks(dec=18, initial_val=3000):
    account = get_account()
    link = LinkToken.deploy({"from": account})
    v3 = MockV3Aggregator.deploy(dec, initial_val, {"from": account})
    vrf = VRFCoordinatorMock.deploy(link.address, {"from": account})
    oracle = MockOracle.deploy(link.address, {"from": account})


def fund_with_link(
    contract_address, account=None, link_token=None, amount=1000000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link")
    tx = interface.LinkTokenInterface(link_token).transfer(
        contract_address, amount, {"from": account}
    )
    print(f"Funded {contract_address}")
    return tx


def get_breed(num):
    num_to_breed = {0: "PUG", 1: "SHIB", 2: "ST_BERNARD"}
    return num_to_breed[num]
