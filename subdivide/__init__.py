"""
Fiona- and geojson-compatible module for interpolating coordinates along lines
"""
from shapely.geometry import shape, mapping
import logging as log
from strategies import preserve_shape
from cut import cut

def subdivide(geometry, interval=1, strategy=preserve_shape):
	"""
	Subdivides line at a given interval
	"""
	geometry = shape(geometry)
	assert geometry.geom_type == "LineString"
	coords = [(p.x, p.y) for p in strategy(geometry,interval)]
	geometry.coords = coords
	return geometry

def subdivide_all(records, interval=1, strategy=preserve_shape):
	"""
	Subdivides line at a given interval
	"""
	for rec in records:
		try:
			assert rec['geometry']['type'] == "LineString"
			geom = shape(rec["geometry"])
			coords = [(p.x, p.y) for p in strategy(geom,interval)]
			rec["geometry"]["coordinates"] = coords

		except Exception, e:
			# Writing untransformed features to a different shapefile
			# is another option.
			log.exception("Error transforming record")
		yield rec
