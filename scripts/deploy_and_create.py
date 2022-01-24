from threading import local
from brownie import accounts, config, network, advnft
from scripts.help import fund_with_link, get_account, get_contract, local_env


def deploy_NFT():
    account = get_account()
    nft = advnft.deploy(
        get_contract("vrf"),
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        get_contract("link"),
        {"from": account},
    )
    fund_with_link(nft.address)
    create = nft.create("twins", {"from": account})
    create.wait(1)
    print(f"deployed NFT to {create}")


def main():
    deploy_NFT()
