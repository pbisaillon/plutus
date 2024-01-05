"""This script is used to manage the dev sqlite database"""

from plutus.db import *
from datetime import date
import typer

# session = get_a_session()

app = typer.Typer()


@app.command()
def build():
    print(f"Building dev database")
    session = getsession()
    add_raw_transaction(
        "Transaction A", "memo A", 127.50, date(2023, 1, 12), 1, session
    )


if __name__ == "__main__":
    app()


def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
