import random
import time

from datetime import datetime, timedelta

import config

from loguru import logger
from eth_account import Account

from src.file_manager import read_wallets_from_file


def mass_refuel():
    wallets = read_wallets_from_file()
    wallets_amount = len(wallets)

    if len(wallets) == 0:
        logger.error("Wallets file is empty, please add wallets to file")
        exit(1)

    wallet_number = 1
    for wallet in wallets:
        refuel = Refuel(private_key=wallet)
        refuel_status = refuel.send_refuel_txn()

        if wallet_number == wallets_amount:
            logger.info(f"Refuel process is finished\n")
            break

        wallet_number += 1

        if refuel_status is not None:
            time_delay = random.randint(config.MIN_DELAY_SECONDS, config.MAX_DELAY_SECONDS)
        else:
            time_delay = 3

        if time_delay == 0:
            time.sleep(0.3)
            continue

        delta = timedelta(seconds=time_delay)
        result_datetime = datetime.now() + delta

        logger.info(f"Waiting {time_delay} seconds, next wallet refuel {result_datetime}\n")
        time.sleep(time_delay)


class Refuel:
    def __init__(self, private_key):
        self.private_key = private_key
        self.source_chain = config.SOURCE_CHAIN
        self.destination_chain = config.DESTINATION_CHAIN
        self.web3 = self.source_chain.web3
        self.wallet_address = self.web3.to_checksum_address(Account.from_key(private_key).address)

    def get_gas_price(self):
        if self.source_chain.chain_name.lower() == 'arbitrum':
            return int(self.web3.eth.gas_price * 1.35)
        elif self.source_chain.chain_name.lower() == 'polygon':
            return int(self.web3.eth.gas_price * 1.35)
        elif self.source_chain.chain_name.lower() == 'avalanche':
            return int(self.web3.eth.gas_price * 1.15)
        else:
            return self.web3.eth.gas_price

    def get_estimate_gas(self, transaction):
        estimated_gas_limit = self.source_chain.web3.eth.estimate_gas(transaction)
        return estimated_gas_limit

    def build_refuel_txn(self, native_amount_out):
        dst_chain_id = self.destination_chain.chain_id
        gas_price = self.get_gas_price()
        nonce = self.web3.eth.get_transaction_count(self.wallet_address)

        refuel_transaction = self.source_chain.refuel_contract.functions.depositNativeToken(
            dst_chain_id,
            self.wallet_address
        ).build_transaction({
            'from': self.wallet_address,
            'value': native_amount_out,
            'gas': config.MAX_GAS_LIMIT,
            'gasPrice': gas_price,
            'nonce': nonce,
        })
        return refuel_transaction

    def get_random_amount_out_native(self, min_amount, max_amount) -> tuple:
        random_amount = random.uniform(min_amount, max_amount)
        random_amount_wei = self.web3.to_wei(random_amount, 'ether')
        return random_amount, random_amount_wei

    def send_refuel_txn(self):
        wallet_balance_wei = self.web3.eth.get_balance(self.wallet_address)
        wallet_balance_decimals = self.web3.from_wei(wallet_balance_wei, 'ether')

        native_amount_out, native_amount_out_wei = self.get_random_amount_out_native(
            min_amount=config.MIN_NATIVE_AMOUNT_OUT,
            max_amount=config.MAX_NATIVE_AMOUNT_OUT)

        if wallet_balance_wei < native_amount_out_wei:
            logger.error(f"[{self.wallet_address}] - Not enough native ({native_amount_out} {self.source_chain.chain_name}) "
                         f"to refuel. Balance: {wallet_balance_decimals} {self.source_chain.chain_name}")
            return

        refuel_txn = self.build_refuel_txn(native_amount_out=native_amount_out_wei)

        try:
            estimated_gas_limit = self.get_estimate_gas(transaction=refuel_txn)
            if config.MAX_GAS_LIMIT > estimated_gas_limit:
                refuel_txn['gas'] = estimated_gas_limit

            if config.TEST_MODE is True:
                logger.info(f"[{self.wallet_address}] - Estimated gas limit: {estimated_gas_limit} for"
                            f" {self.source_chain.chain_name} → {self.destination_chain.chain_name} refuel")
                return

            signed_txn = self.web3.eth.account.sign_transaction(refuel_txn, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.success(f"[{self.wallet_address}] - {self.source_chain.chain_name} → {self.destination_chain.chain_name}"
                           f" refuel transaction sent (Native amount: {native_amount_out}): {txn_hash.hex()}")
            return txn_hash.hex()

        except Exception as e:
            logger.error(f"[{self.wallet_address}] - Error while sending ETH bridge txn: {e}")
            return
