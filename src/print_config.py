import config
import time

from loguru import logger


def print_config():
    logger.debug(f"Created by https://github.com/frankmurrey (tg @shnubjack)\n")
    delay = 5

    logger.info(f"Starting refuel process in {delay} sec\n")
    logger.info(f"Config:")
    logger.warning(f"Source chain: {config.SOURCE_CHAIN.chain_name}")
    logger.warning(f"Destination chain: {config.DESTINATION_CHAIN.chain_name}")
    logger.warning(f"Min amount to refuel: {config.MIN_NATIVE_AMOUNT_OUT}")
    logger.warning(f"Max amount to refuel: {config.MAX_NATIVE_AMOUNT_OUT}")
    logger.warning(f"Min delay: {config.MIN_DELAY_SECONDS}")
    logger.warning(f"Max delay: {config.MAX_DELAY_SECONDS}")
    logger.warning(f"Max gas limit: {config.MAX_GAS_LIMIT}")
    logger.warning(f"Test mode: {config.TEST_MODE}\n")
    logger.warning(f"Press Ctrl+C to stop refuel process\n")
    time.sleep(delay)

