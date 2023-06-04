import json

from src.paths import RPCS_FILE

with open(RPCS_FILE, "r") as file:
    all_rpcs = json.load(file)

