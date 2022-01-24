from distutils.command.upload import upload
from brownie import advnft, config, network
from brownie.network.main import show_active
from scripts.help import get_account
from scripts.help import fund_with_link, get_account, get_contract, local_env, get_breed
from scripts.upload_to_pinata import pinata
from web3 import Web3
from pathlib import Path
from metadata.metadata_template import metadata_template
import requests, json


def main():
    nft = advnft[-1]
    print(nft)
    num_nfts = nft.tokencounter()
    print(f"youve created {num_nfts}")
    for token_id in range(num_nfts):
        breed = get_breed(nft.tokenidbreed(token_id))
        meta_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        nft_metadata = metadata_template
        # if Path(meta_file_name).exists():
        #   print(f"{meta_file_name} already exists")
        print(f"creating metadata file for {meta_file_name}")
        nft_metadata["name"] = breed
        nft_metadata["description"] = f"an adorable {breed} pup"
        image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
        image_uri = upload_to_ipfs(image_path)
        nft_metadata["image"] = image_uri
        with open(meta_file_name, "w") as file:
            json.dump(nft_metadata, file)
        meta_data_upload = upload_to_ipfs(nft_metadata)
        print(meta_data_upload)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(image_uri)
    return image_uri
