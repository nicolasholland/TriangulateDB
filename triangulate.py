import pandas as pd
import handle_db
from scipy.spatial import Delaunay


class TriangulateDB(object):

    def __init__(self) -> None:
        self.dbh = handle_db.DBHandle()

    def create_triangulation(self):
        get_geotable = self.dbh.get_geotable()
        triangulation = Delaunay(
            list(get_geotable.apply(
                lambda geom: (geom.latitude, geom.longitude), axis=1)))
        return triangulation

    @staticmethod
    def get_vertices(triangulation, latitude, longitude):
        triangle_idx = triangulation.find_simplex([[latitude, longitude]])

        if triangle_idx == -1:
            # The location is outside the triangulation
            raise ValueError("The location is outside the triangulation.")

        vertex_indices = triangulation.simplices[triangle_idx].reshape(3).tolist()
        return vertex_indices

    def get_ts_from_vertices(self, geo, vertex_indices):
        geoids = list(geo.iloc[vertex_indices].uuid)

        retval = [self.dbh.get_ts(geoid) for geoid in geoids]

        return retval

    @staticmethod
    def barycentric_interpolation(triangulation, vertex_indices, latitude, longitude):
        triangle_vertices = triangulation.points[vertex_indices]
        print("triangle_vertices ", triangle_vertices)
        v0, v1, v2 = triangle_vertices
        denom = (v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1])
        b0 = ((v1[1] - v2[1]) * (longitude - v2[0]) + (v2[0] - v1[0]) * (latitude - v2[1])) / denom
        b1 = ((v2[1] - v0[1]) * (longitude - v2[0]) + (v0[0] - v2[0]) * (latitude - v2[1])) / denom
        b2 = 1.0 - b0 - b1

        return b0, b1, b2

    @staticmethod
    def interpolate(timeseries, weights):
        retval = timeseries[0] * weights[0]
        retval += timeseries[1] * weights[1]
        retval += timeseries[2] * weights[2]

        return retval

def main(latitude, longitude):
    tdb = TriangulateDB()

    geo = tdb.dbh.get_geotable()
    triangulation = tdb.create_triangulation()

    vertex_indices = tdb.get_vertices(triangulation, latitude, longitude)

    timeseries = tdb.get_ts_from_vertices(geo, vertex_indices)
    parameters = tdb.barycentric_interpolation(
        triangulation, vertex_indices, latitude, longitude)

    val = tdb.interpolate(timeseries, parameters)
    
    return val


if __name__ == '__main__':
    latitude, longitude = 21.194765442951883, 96.58275260684468
    main(latitude, longitude)

