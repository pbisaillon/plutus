"""This script is used to populate the dev sqlite database"""

from plutus.db import *
from datetime import date

session = get_a_session()

add_raw_transaction("Transaction A", "memo A", 127.50, date(2023, 1, 12), 1, session)
