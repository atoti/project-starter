from __future__ import annotations

from .util import (
    Column,
    Columns,
    Cube,
    Cubes,
    Dimension,
    Dimensions,
    Hierarchies,
    Hierarchy,
    Level,
    Levels,
    Measure,
    Measures,
    Table,
    Tables,
)


class _StationDetailsTableColumns(Columns):
    ID = Column("ID")
    NAME = Column("Name")
    DEPARTMENT = Column("Department")
    CITY = Column("City")
    POSTCODE = Column("Postcode")
    STREET = Column("Street")
    HOUSE_NUMBER = Column("House number")
    CAPACITY = Column("Capacity")


class _StationDetailsTable(Table):
    name = "Station details"
    columns = _StationDetailsTableColumns()


class _StationStatusTableColumn(Columns):
    STATION_ID = Column("Station ID")
    BIKE_TYPE = Column("Bike type")
    BIKES = Column("Bikes")


class _StationStatusTable(Table):
    name = "Station status"
    columns = _StationStatusTableColumn()


class _Tables(Tables):
    STATION_DETAILS = _StationDetailsTable()
    STATION_STATUS = _StationStatusTable()


class _StationCubeMeasures(Measures):
    CAPACITY = Measure(_StationDetailsTableColumns.CAPACITY.name)
    BIKES = Measure(_StationStatusTableColumn.BIKES.name)


class _StationCubeStationDetailsDimensionLocationHierarchyLevels(Levels):
    DEPARTMENT = Level(_StationDetailsTable.columns.DEPARTMENT.name)
    CITY = Level(_StationDetailsTable.columns.CITY.name)
    POSTCODE = Level(_StationDetailsTable.columns.POSTCODE.name)
    STREET = Level(_StationDetailsTable.columns.STREET.name)
    HOUSE_NUMBER = Level(_StationDetailsTable.columns.HOUSE_NUMBER.name)


class _StationCubeStationDetailsDimensionLocationHierarchy(Hierarchy):
    name = "Location"
    levels = _StationCubeStationDetailsDimensionLocationHierarchyLevels()


class _StationCubeStationDetailsDimensionStationHierarchyLevels(Levels):
    NAME = Level(_StationDetailsTable.columns.NAME.name)
    ID = Level(_StationDetailsTable.columns.ID.name)


class _StationCubeStationDetailsDimensionStationHierarchy(Hierarchy):
    name = "Station"
    levels = _StationCubeStationDetailsDimensionStationHierarchyLevels()


class _StationCubeStationDetailsDimensionHierarchies(Hierarchies):
    LOCATION = _StationCubeStationDetailsDimensionLocationHierarchy()
    STATION = _StationCubeStationDetailsDimensionStationHierarchy()


class _StationCubeStationDetailsDimension(Dimension):
    name = _StationDetailsTable.name
    hierarchies = _StationCubeStationDetailsDimensionHierarchies()


class _StationCubeStationStatusDimensionBikeTypeHierarchyLevels(Levels):
    BIKE_TYPE = Level(_StationStatusTableColumn.BIKE_TYPE.name)


class _StationCubeStationStatusDimensionBikeTypeHierarchy(Hierarchy):
    name = "Bike type"
    levels = _StationCubeStationStatusDimensionBikeTypeHierarchyLevels()


class _StationCubeStationStatusDimensionHierarchies(Hierarchies):
    BIKE_TYPE = _StationCubeStationStatusDimensionBikeTypeHierarchy()


class _StationCubeStationStatusDimension(Dimension):
    name = _StationStatusTable.name
    hierarchies = _StationCubeStationStatusDimensionHierarchies()


class _StationCubeDimensions(Dimensions):
    STATION_DETAILS = _StationCubeStationDetailsDimension()
    STATION_STATUS = _StationCubeStationStatusDimension()


class _StationCube(Cube):
    name = "Station"
    measures = _StationCubeMeasures()
    dimensions = _StationCubeDimensions()


class _Cubes(Cubes):
    STATION = _StationCube()


class _Structure:
    tables = _Tables()
    cubes = _Cubes()


STRUCTURE = _Structure()


STRUCTURE.cubes.STATION.dimensions.STATION_DETAILS.hierarchies.STATION.levels.NAME.key
