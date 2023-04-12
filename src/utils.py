import asyncio
from typing import Union

from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair

from src.constants import CHAIN_ID, GATEWAY_CLIENT, STARKSCAN_URL


def int_to_uint256(value):
    value = int(value)
    low = value & ((1 << 128) - 1)
    high = value >> 128
    return {"low": low, "high": high}


def parse_int(value: Union[int, str]) -> int:
    if isinstance(value, int):
        return value
    if value == "":
        return 0
    base = 16 if isinstance(value, str) and value[:2] == "0x" else 10
    return int(value, base)


def get_account(
    address,
    private_key,
) -> Account:
    address = int(address, 16)
    key_pair = KeyPair.from_private_key(int(private_key, 16))
    return Account(
        address=address,
        client=GATEWAY_CLIENT,
        chain=CHAIN_ID,
        key_pair=key_pair,
    )


def get_tx_url(tx_hash: int) -> str:
    return f"{STARKSCAN_URL}/tx/0x{tx_hash:064x}"


def sync(f):
    def _f(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return _f
