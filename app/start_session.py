import os
import atoti as tt
import pandas as pd


def start_session():
    session = tt.create_session(
        config={
            "user_content_storage": "content",
            "port": int(os.getenv("PORT") or 9090),
            "java_options": ["-Xmx250m"],
        }
    )
    table = session.read_pandas(
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
    session.create_cube(table)
    return session
