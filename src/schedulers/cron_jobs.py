import json
import logging

import numpy as np
import pandas as pd
from starknet_py.net.client_models import Call
from starkware.starknet.public.abi import get_selector_from_name

from src.constants import GATEWAY_CLIENT, NETWORK
from src.spreadsheet import DriveClient
from src.utils import get_account, get_tx_url, parse_int

drive_client = DriveClient()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def call_job():
    accounts = drive_client.get_sheet_as_dataframe("Accounts")
    calls = (
        drive_client.get_sheet_as_dataframe("Calls")
        .assign(
            to_addr=lambda df: df.to_addr.map(parse_int),
            selector=lambda df: np.where(
                df.selector == "",
                df.selector_name.map(get_selector_from_name),
                df.selector.map(parse_int),
            ),
            calldata=lambda df: df.calldata.str.split(",").map(
                lambda args: [parse_int(arg) for arg in args]
            ),
        )
        .drop("selector_name", axis=1)
        .agg(
            lambda row: Call(**row),
            axis=1,
        )
        .tolist()
    )
    if not calls:
        logger.info(f"ℹ️  No calls for network {NETWORK}")
        return

    logger.info(f"ℹ️  {len(calls)} calls found for {NETWORK}")
    logger.info(f"ℹ️  Sending tx for {len(accounts)} accounts")
    txs = [
        await get_account(**account).execute(calls, max_fee=int(1e16))
        for account in accounts.to_dict("records")
    ]

    logger.info(
        f"⏳ Waiting for txs:\n{json.dumps([get_tx_url(tx.transaction_hash) for tx in txs], indent=2)}"
    )
    receipts = [await GATEWAY_CLIENT.wait_for_tx(tx.transaction_hash) for tx in txs]
    pd.DataFrame(
        {
            "hash": [get_tx_url(tx.transaction_hash) for tx in txs],
            "from": accounts.address,
            "status": [r[1].name for r in receipts],
        }
    ).agg(lambda row: drive_client.append_series_to_sheet("Transactions", row), axis=1)
