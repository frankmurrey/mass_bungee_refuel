import pathlib
import os

MAIN_DIR = os.path.join(pathlib.Path(__file__).parent.parent.resolve())
CONFIG_FILE = os.path.join(MAIN_DIR, "config_manual.yaml")
CONTRACTS_DIR = os.path.join(MAIN_DIR, "contracts")
RPCS_FILE = os.path.join(MAIN_DIR, "rpcs.json")
WALLETS_FILE = os.path.join(MAIN_DIR, "wallets.txt")

class Arbdir:
    CHAIN_DIR = os.path.join(CONTRACTS_DIR, "arbitrum")
    ABIS_DIR = os.path.join(CHAIN_DIR, "abis")
    REFUEL_ABI_FILE = os.path.join(ABIS_DIR, "refuel.abi")


class AvalancheDir:
    CHAIN_DIR = os.path.join(CONTRACTS_DIR, "avalanche")
    ABIS_DIR = os.path.join(CHAIN_DIR, "abis")
    REFUEL_ABI_FILE = os.path.join(ABIS_DIR, "refuel.abi")


class BscDir:
    CHAIN_DIR = os.path.join(CONTRACTS_DIR, "bsc")
    ABIS_DIR = os.path.join(CHAIN_DIR, "abis")
    REFUEL_ABI_FILE = os.path.join(ABIS_DIR, "refuel.abi")


class PolygonDir:
    CHAIN_DIR = os.path.join(CONTRACTS_DIR, "polygon")
    ABIS_DIR = os.path.join(CHAIN_DIR, "abis")
    REFUEL_ABI_FILE = os.path.join(ABIS_DIR, "refuel.abi")


class FantomDir:
    CHAIN_DIR = os.path.join(CONTRACTS_DIR, "fantom")
    ABIS_DIR = os.path.join(CHAIN_DIR, "abis")
    REFUEL_ABI_FILE = os.path.join(ABIS_DIR, "refuel.abi")