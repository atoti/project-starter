from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import timedelta
from pathlib import Path
from typing import Any, cast

import atoti as tt
import pandas as pd
from pydantic import HttpUrl

from .config import Config
from .structure import STRUCTURE
from .util import read_json, reverse_geocode


def read_station_details(
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
    velib_data_base_path: HttpUrl | Path,
) -> pd.DataFrame:
    station_details_columns = STRUCTURE.tables.STATION_DETAILS.columns

    stations_data: Any = cast(
        Any,
        read_json(
            velib_data_base_path, Path("station_information.json"), timeout=timeout
        ),
    )["data"]["stations"]
    station_information_df = pd.DataFrame(stations_data)[
        ["station_id", "name", "capacity", "lat", "lon"]
    ].rename(
        columns={
            "station_id": station_details_columns.ID.name,
            "name": station_details_columns.NAME.name,
            "capacity": station_details_columns.CAPACITY.name,
            "lat": "latitude",
            "lon": "longitude",
        }
    )

    coordinates_column_names = ["latitude", "longitude"]

    coordinates = cast(
        Iterable[tuple[float, float]],
        station_information_df[coordinates_column_names].itertuples(
            index=False, name=None
        ),
    )

    reverse_geocoded_df = reverse_geocode(
        coordinates, reverse_geocoding_path=reverse_geocoding_path, timeout=timeout
    ).rename(
        columns={
            "department": station_details_columns.DEPARTMENT.name,
            "city": station_details_columns.CITY.name,
            "postcode": station_details_columns.POSTCODE.name,
            "street": station_details_columns.STREET.name,
            "house_number": station_details_columns.HOUSE_NUMBER.name,
        }
    )

    return station_information_df.merge(
        reverse_geocoded_df, how="left", on=coordinates_column_names
    ).drop(columns=coordinates_column_names)


def read_station_status(
    velib_data_base_path: HttpUrl | Path,
    /,
    *,
    timeout: timedelta,
) -> pd.DataFrame:
    station_status_columns = STRUCTURE.tables.STATION_STATUS.columns

    stations_data = cast(
        Any,
        read_json(velib_data_base_path, Path("station_status.json"), timeout=timeout),
    )["data"]["stations"]
    station_statuses: list[Mapping[str, Any]] = []
    for station_status in stations_data:
        for num_bikes_available_types in station_status["num_bikes_available_types"]:
            if len(num_bikes_available_types) != 1:
                raise ValueError(
                    f"Expected a single bike type but found: {list(num_bikes_available_types.keys())}"
                )
            bike_type, bikes = next(iter(num_bikes_available_types.items()))
            station_statuses.append(
                {
                    station_status_columns.STATION_ID.name: station_status[
                        "station_id"
                    ],
                    station_status_columns.BIKE_TYPE.name: bike_type,
                    station_status_columns.BIKES.name: bikes,
                }
            )
    return pd.DataFrame(station_statuses)


def load_tables(session: tt.Session, /, *, config: Config) -> None:
    station_details_df = read_station_details(
        reverse_geocoding_path=config.reverse_geocoding_path,
        timeout=config.requests_timeout,
        velib_data_base_path=config.velib_data_base_path,
    )
    station_status_df = read_station_status(
        config.velib_data_base_path,
        timeout=config.requests_timeout,
    )

    with session.start_transaction():
        session.tables[STRUCTURE.tables.STATION_DETAILS.name].load_pandas(
            station_details_df
        )
        session.tables[STRUCTURE.tables.STATION_STATUS.name].load_pandas(
            station_status_df
        )
