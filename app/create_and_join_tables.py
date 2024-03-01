from __future__ import annotations

import atoti as tt

from .structure import STRUCTURE
from .util import get_column


def create_station_status_table(session: tt.Session, /) -> None:
    structure = STRUCTURE.tables.STATION_STATUS
    columns = structure.columns
    session.create_table(
        structure.name,
        keys=[columns.STATION_ID.name, columns.BIKE_TYPE.name],
        types={
            columns.STATION_ID.name: "long",
            columns.BIKE_TYPE.name: "String",
            columns.BIKES.name: "int",
        },
    )


def create_station_details_table(session: tt.Session, /) -> None:
    structure = STRUCTURE.tables.STATION_DETAILS
    columns = structure.columns
    session.create_table(
        structure.name,
        keys=[columns.ID.name],
        types={
            columns.ID.name: "long",
            columns.NAME.name: "String",
            columns.DEPARTMENT.name: "String",
            columns.CITY.name: "String",
            columns.POSTCODE.name: "int",
            columns.STREET.name: "String",
            columns.HOUSE_NUMBER.name: "String",
            columns.CAPACITY.name: "int",
        },
        default_values={columns.POSTCODE.name: 0},
    )


def join_tables(session: tt.Session, /) -> None:
    session.tables[STRUCTURE.tables.STATION_STATUS.name].join(
        session.tables[STRUCTURE.tables.STATION_DETAILS.name],
        get_column(STRUCTURE.tables.STATION_STATUS.columns.STATION_ID, session=session)
        == get_column(STRUCTURE.tables.STATION_DETAILS.columns.ID, session=session),
    )


def create_and_join_tables(session: tt.Session, /) -> None:
    create_station_status_table(session)
    create_station_details_table(session)
    join_tables(session)
