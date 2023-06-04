import json

from web3 import Web3
from loguru import logger

from src.paths import FantomDir
from src.rpcs import all_rpcs


with open(FantomDir.REFUEL_ABI_FILE, "r") as file:
    REFUEL_ABI = json.load(file)


class Fantom:
    def __init__(self):
        self.chain_id: int = 250
        self.chain_name = "Fantom"

        if len(all_rpcs[self.chain_name]) == 0:
            logger.error(f"Please provide at least one valid rpc for {self.chain_name}")
            exit(1)

        self.web3 = Web3(Web3.HTTPProvider(all_rpcs[self.chain_name][0]))

        self.refuel_address = self.web3.to_checksum_address("0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB")
        self.refuel_abi = REFUEL_ABI
        self.refuel_contract = self.web3.eth.contract(address=self.refuel_address, abi=self.refuel_abi)

