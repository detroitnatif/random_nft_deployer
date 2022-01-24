from brownie import advnft, config, network
from scripts.help import get_account
from scripts.help import fund_with_link, get_account, get_contract, local_env, get_breed
from web3 import Web3
from pathlib import Path
from metadata.metadata_template import metadata_template
import requests
import os


def pinata(name):
    pinata_base = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    filepath = f"./img/{name}.png"
    filename = filepath.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            pinata_base + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
        print(
            f"uploaded to https://gateway.pinata.cloud/ipfs/{response.json()['IpfsHash']}?preview=1"
        )


def main():
    pinata("st-bernard")
