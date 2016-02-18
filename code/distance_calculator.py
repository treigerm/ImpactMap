import math

def calculateDistance (lat1,lon1,lat2,lon2):
	# Earth radius
	r = 6371

	dLat = math.radians(lat2-lat1)
	dLon = math.radians(lon2-lon1)
	lat1 = math.radians(lat1)
	lat2 = math.radians(lat2)

	a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
	c = 2 * math.atan2(math.sqrt(a),math.sqrt(1 - a))
	d = r * c

	return d

def calculateArea (minLat,maxLat,minLon,maxLon):
	sideA = calculateDistance(minLat,minLon,minLat,maxLon)
	sideB = calculateDistance(minLat,minLon,maxLat,minLon)

	area = sideA * sideB

	return area

# command-line checker
print calculateArea(40.997960, 45.001321, -111.055199, -104.057697)