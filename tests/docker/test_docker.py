from __future__ import annotations

import atoti as tt

from app import STRUCTURE


def test_query_session_inside_docker_container(
    query_session_inside_docker_container: tt.QuerySession,
) -> None:
    cube = query_session_inside_docker_container.cubes[STRUCTURE.cubes.STATION.name]
    result_df = cube.query(cube.measures["contributors.COUNT"])
    assert result_df["contributors.COUNT"][0] > 0
