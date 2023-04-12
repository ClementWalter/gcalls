# coding=UTF-8
import logging
import os
from datetime import datetime

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

from src.constants import NETWORK
from src.schedulers.cron_jobs import call_job
from src.utils import sync

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("apscheduler").setLevel(logging.INFO)

# Cron info
HOUR = int(os.getenv("HOUR", 0))
MINUTE = int(os.getenv("MINUTE", 0))
SECOND = int(os.getenv("SECOND", 10))
JITTER = int(os.getenv("JITTER", 0))


if __name__ == "__main__":
    logging.info(f"Gcall started on network {NETWORK}")
    offset = pytz.timezone("Europe/Paris").utcoffset(datetime.now()).total_seconds()
    scheduler = BlockingScheduler()
    scheduler.add_job(
        sync(call_job), "interval", hours=HOUR, minutes=MINUTE, seconds=SECOND, jitter=JITTER
    )
    scheduler.start()
