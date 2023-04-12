import os
import re
from enum import Enum

from dotenv import load_dotenv
from starknet_py.net.gateway_client import GatewayClient

load_dotenv()

NETWORK = os.getenv("STARKNET_NETWORK", "starknet-devnet")
NETWORK = (
    "testnet"
    if re.match(r".*(testnet|goerli)$", NETWORK, flags=re.I)
    else "testnet2"
    if re.match(r".*(testnet|goerli)-?2$", NETWORK, flags=re.I)
    else "devnet"
    if re.match(r".*(devnet|local).*", NETWORK, flags=re.I)
    else "mainnet"
)
GATEWAY_URLS = {
    "mainnet": "https://alpha-mainnet.starknet.io",
    "testnet": "https://alpha4.starknet.io",
    "testnet2": "https://alpha4-2.starknet.io",
    "devnet": "http://127.0.0.1:5050",
}
GATEWAY_CLIENT = GatewayClient(net=GATEWAY_URLS[NETWORK])
STARKNET_NETWORKS = {
    "mainnet": "alpha-mainnet",
    "testnet": "alpha-goerli",
    "testnet2": "alpha-goerli2",
    "devnet": "alpha-goerli",
}
STARKNET_NETWORK = STARKNET_NETWORKS[NETWORK]
STARKSCAN_URLS = {
    "mainnet": "https://starkscan.co",
    "testnet": "https://testnet.starkscan.co",
    "testnet2": "https://testnet-2.starkscan.co",
    "devnet": "https://devnet.starkscan.co",
}
STARKSCAN_URL = STARKSCAN_URLS[NETWORK]


class ChainId(Enum):
    mainnet = int.from_bytes(b"SN_MAIN", "big")
    testnet = int.from_bytes(b"SN_GOERLI", "big")
    testnet2 = int.from_bytes(b"SN_GOERLI2", "big")
    devnet = int.from_bytes(b"SN_GOERLI", "big")


CHAIN_ID = getattr(ChainId, NETWORK)
