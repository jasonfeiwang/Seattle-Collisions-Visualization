"""
Function to read the neighborhood data for Seattle
and assign it to collisions.

This file reads the geojson file and provides an interface which
given a dataframe containing latitudes and longitudes, assigns
Seattle neighbourhoods to them
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point

NEIGHBORHOODS = gpd.read_file('../wa_collisions/data/Neighborhoods/Neighborhoods.json')
NEIGHBORHOODS_COUNT = len(NEIGHBORHOODS)

def get_neighborhood(latitude, longitude):
    """
    Returns the Object ID for the Seattle neighborhood for a
    given latitude and longitude.

    Returns -1 if the location is not in any Seattle
    neighborhood

    Args:
        latitude (float): latitude of the location
        longitude (float): longitude of the location

    Returns:
        object_id (int): object id of the seattle
        neighborhood. object_id varies from 1 to 119
        (inclusive). Returns -1 if the location is not
        in any Seattle neighborhood.

    Raises:
        ValueError: if the latitude or longitude can't be
            converted into float
    """
    location_point = Point(float(latitude), float(longitude))
    for i in range(0, NEIGHBORHOODS_COUNT):
        if NEIGHBORHOODS['geometry'][i].contains(location_point):
            return NEIGHBORHOODS['OBJECTID'][i]
    return -1


def assign_neighborhood(dataframe):
    """
    Returns the provided dataframe with an additional column
    object_id which contains the object id of the seattle
    neighborhood of the location in the dataframe.

    The dataframe must have columns X and Y for the location.

    Args:
        dataframe(pandas dataframe): dataframe containing the
            locations in seattle. Must have columns X and Y

    Returns:
        dataframe(pandas dataframe): the provided dataframe with an
            added column "object_id" containing the object id of the
            neighborhood in seattle the location is present in. If the
            location is in't any of the neighborhood, the column
            contains the value -1.

    Raises:
        ValueError: if the dataframe doesn't contain the columns
            X or Y.
        ValueError: if the X or Y can't be
            converted into float
    """
    if not 'X' in dataframe.columns:
        raise ValueError("Dataframe doesn't have a column X")
    if not 'Y' in dataframe.columns:
        raise ValueError("Dataframe doesn't have a column Y")

    object_ids = np.zeros(len(dataframe))
    for i in range(0, len(object_ids)):
        object_ids[i] = get_neighborhood(dataframe['X'][i], dataframe['Y'][i])

    dataframe['object_id'] = object_ids
    return dataframe
