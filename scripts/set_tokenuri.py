from lib2to3.pgen2 import token
from brownie import accounts, config, network, advnft
from scripts.help import fund_with_link, get_account, get_contract, local_env, get_breed

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"working on {network.show_active()}")
    nft = advnft[-1]
    num_of_nfts = nft.tokencounter()
    print(f"you have created {num_of_nfts}")
    for token_id in range(num_of_nfts):
        breed = get_breed(nft.tokenidbreed(token_id))
        if not nft.tokenURI(token_id).startswith("https://"):
            print(f"setting tokenURI of {token_id}")
            set_token_uri(token_id, nft, dog_metadata_dic[breed])


def set_token_uri(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
