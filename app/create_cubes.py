from __future__ import annotations

import atoti as tt

from .structure import STRUCTURE
from .util import get_column


def create_station_cube(session: tt.Session, /) -> None:
    station_details_columns = STRUCTURE.tables.STATION_DETAILS.columns
    station_status_columns = STRUCTURE.tables.STATION_STATUS.columns

    structure = STRUCTURE.cubes.STATION
    dimensions, measures = structure.dimensions, structure.measures

    cube = session.create_cube(
        session.tables[STRUCTURE.tables.STATION_STATUS.name],
        structure.name,
        mode="manual",
    )
    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h.update(
        {
            dimensions.STATION_STATUS.hierarchies.BIKE_TYPE.key: {
                dimensions.STATION_STATUS.hierarchies.BIKE_TYPE.levels.BIKE_TYPE.name: get_column(
                    station_status_columns.BIKE_TYPE, session=session
                )
            },
            dimensions.STATION_DETAILS.hierarchies.LOCATION.key: {
                dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.DEPARTMENT.name: get_column(
                    station_details_columns.DEPARTMENT, session=session
                ),
                dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.CITY.name: get_column(
                    station_details_columns.CITY, session=session
                ),
                dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.POSTCODE.name: get_column(
                    station_details_columns.POSTCODE, session=session
                ),
                dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.STREET.name: get_column(
                    station_details_columns.STREET, session=session
                ),
                dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.HOUSE_NUMBER.name: get_column(
                    station_details_columns.HOUSE_NUMBER, session=session
                ),
            },
            dimensions.STATION_DETAILS.hierarchies.STATION.key: {
                dimensions.STATION_DETAILS.hierarchies.STATION.levels.NAME.name: get_column(
                    station_details_columns.NAME, session=session
                ),
                dimensions.STATION_DETAILS.hierarchies.STATION.levels.ID.name: get_column(
                    station_status_columns.STATION_ID, session=session
                ),
            },
        }
    )

    m.update(
        {
            measures.BIKES: tt.agg.sum(
                get_column(station_status_columns.BIKES, session=session)
            ),
            measures.CAPACITY: tt.agg.sum(
                tt.agg.single_value(
                    get_column(station_details_columns.CAPACITY, session=session)
                ),
                scope=tt.OriginScope(
                    l[dimensions.STATION_DETAILS.hierarchies.STATION.levels.ID.key]
                ),
            ),
        }
    )


def create_cubes(session: tt.Session, /) -> None:
    create_station_cube(session)
