from __future__ import annotations

import atoti as tt

from .structure import Column


def get_column(column: Column, /, *, session: tt.Session) -> tt.Column:
    table_name, column_name = column.key
    return session.tables[table_name][column_name]
