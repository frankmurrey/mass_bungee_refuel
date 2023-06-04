import contracts


# Choose the chains to use, available: "bsc", "polygon", "fantom", "arbitrum", "avalanche
SOURCE_CHAIN = contracts.polygon
DESTINATION_CHAIN = contracts.bsc

# Choose native token amount to refuel, will be randomized between min and max
MIN_NATIVE_AMOUNT_OUT = 0.01
MAX_NATIVE_AMOUNT_OUT = 0.02

# Choose delay between refuel transactions, will be randomized between min and max
MIN_DELAY_SECONDS = 10
MAX_DELAY_SECONDS = 20

# Choose max gas limit for refuel transactions, will ebe chosen optimal by 'estimate_gas'
MAX_GAS_LIMIT = 300000000

# Test mode will not send transactions, only print estimated gas (True/False)
TEST_MODE = True
