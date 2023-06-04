from src.paths import WALLETS_FILE

from loguru import logger


def create_empty_wallets_file():
    with open(WALLETS_FILE, "w") as file:
        file.write("")
        logger.info("Created evm wallets file")


def read_wallets_from_file():
    try:
        with open(WALLETS_FILE, "r") as file:
            wallets_from_txt = file.read().splitlines()
            if wallets_from_txt is None:
                return []
            return [x for x in wallets_from_txt if x and x.strip() and len(x) == 66]
    except FileNotFoundError:
        logger.error("Wallets file not found")
        create_empty_wallets_file()
        return []