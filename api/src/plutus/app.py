from typing import Union
from plutus.db import *
from litestar import Litestar, get


@get("/")
async def get_list() -> str:
    # get a session
    session = get_a_session()
    tr = get_transaction(1, session)

    return f"Name {tr.description} at {tr.date} - {tr.amount}$"


app = Litestar([get_list])
