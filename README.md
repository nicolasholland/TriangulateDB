TriangulateDB
=============

This repo contains a demo for our TriangulateDB idea.
You can read time series, eg from .epw files and fill a database with them:

```
$ python handle_epw.py VNM_HANOI_HadCM3-A2-2050.epw 21.26347411413358 105.63912300232661
```

The database contains one table where each location is stored using a unique ide (uuid)
and its geocoordinates.
Also the timeseries are stored in separate tables referenced by the uuid.

Once one has filled the database with as many timeseries / location as one has,
the service can be started:


```
$ python app.py
```

This will start a flask server on http://localhost:5000
The service displays a map with all the locations from the database displayed.
The timeseries of the locations can be plotted and there is an endpoint,
which can eg be adressed via the gui.
This endpoint takes a latitude and longitude coordinate, computes a Delaunay
triangulation of the available locations and calculates a barycentric interpolation
for the requested coordinate.
That way new data can easily be generated for any location within the grid of provided
timeseries data.
The more locations one adds to the database, the more accurate are the results of the
barycentric interpolation.




