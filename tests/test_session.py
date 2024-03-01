from __future__ import annotations

import atoti as tt
import pandas as pd

from app import STRUCTURE


def test_total_capacity(session: tt.Session) -> None:
    CUBE = STRUCTURE.cubes.STATION
    station_cube = session.cubes[CUBE.name]
    m = station_cube.measures
    result = station_cube.query(m[CUBE.measures.CAPACITY])
    expected_result = pd.DataFrame(
        columns=[CUBE.measures.CAPACITY],
        data=[
            (45_850),
        ],
        dtype="Int32",
    )
    pd.testing.assert_frame_equal(result, expected_result)


def test_departments(session: tt.Session) -> None:
    CUBE = STRUCTURE.cubes.STATION
    station_cube = session.cubes[CUBE.name]
    l, m = station_cube.levels, station_cube.measures
    result = station_cube.query(
        m["contributors.COUNT"],
        levels=[
            l[
                CUBE.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.DEPARTMENT.key
            ]
        ],
    )
    assert list(result.index) == [
        "75, Paris, Île-de-France",
        "92, Hauts-de-Seine, Île-de-France",
        "93, Seine-Saint-Denis, Île-de-France",
        "94, Val-de-Marne, Île-de-France",
        "95, Val-d'Oise, Île-de-France",
    ]
