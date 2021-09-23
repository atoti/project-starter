import os
import re
from typing import Mapping

import atoti as tt
import pandas as pd

HEROKU_DATABASE_URL_PATTERN = (
    r"(?P<database>postgres://)(?P<username>.*):(?P<password>.*)@(?P<url>.*)"
)


def start_session():
    session = tt.create_session(
        config={
            **{
                "port": int(
                    os.getenv("PORT") or 9090
                ),  # port assigned by Heroku for the application
                "java_options": ["-Xmx250m"],
            },
            **_get_content_storage_config(),
        }
    )
    store = session.read_pandas(
        pd.DataFrame(
            columns=["Product", "Price"],
            data=[
                ("car", 20000.0),
                ("computer", 1000.0),
                ("phone", 500.0),
                ("game", 60.0),
            ],
        ),
        table_name="Products",
    )
    session.create_cube(store)
    return session


def _get_content_storage_config() -> Mapping[str, Mapping[str, str]]:
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        return {}
    match = re.match(HEROKU_DATABASE_URL_PATTERN, database_url)
    if match is None:
        raise ValueError("Failed to parse database URL")
    username = match.group("username")
    password = match.group("password")
    url = match.group("url")
    if not "postgres" in match.group("database"):
        raise ValueError(f"Expected Postgres database, got {match.group('database')}")
    return {
        "user_content_storage": {
            "url": f"postgresql://{url}?user={username}&password={password}"
        }
    }
