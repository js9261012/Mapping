from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt, pi

import json

# Create your views here.
# 
def decimal_default(obj):
	if isinstance(obj, Decimal):
		return float(obj)

def caldistance(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 

	# 6367 km is the radius of the Earth
	km = 6371 * c
	return km


def calnewlnglat(latitude, longitude, dx, dy):
	r_earth = 6371.0
	new_latitude  = latitude  + (Decimal(dy) / Decimal(r_earth)) * (Decimal(180.0) / Decimal(pi))
	new_longitude = longitude + (Decimal(dx) / Decimal(r_earth)) * (Decimal(180.0) / Decimal(pi)) / Decimal(cos(latitude * Decimal(pi)/Decimal(180.0)))
	return new_latitude, new_longitude

def isBound(lng, lat, boubd_left_lng, bound_right_lng, bound_up_lat, bound_down_lat):

	# Calculate the longitude is out of left or right bound
	# Calculate the latitude is out of upper or lower bound
	# Using "and" for smaller bound, "or" for larger bound
	if (lng < bound_right_lng and lng > boubd_left_lng) and (lat < bound_up_lat and lat > bound_down_lat):
		return True
	return False

def route(request):
	# In here, the distance is now killometers
	center_lng = request.GET.get('c_lng', '')
	center_lat = request.GET.get('c_lat', '')
	boubd_left_lng = request.GET.get('b_left_lng', '')
	bound_right_lng = request.GET.get('b_right_lng', '')
	bound_up_lat = request.GET.get('b_up_lat', '')
	bound_down_lat = request.GET.get('b_down_lat', '')

	# meter, has to change to km for cal
	radius = request.GET.get('r', '')

	if center_lat is '': 
		return HttpResponse(status=204)
	elif center_lng is '':
		return HttpResponse(status=204)
	elif boubd_left_lng is '':
		return HttpResponse(status=204)
	elif bound_right_lng is '':
		return HttpResponse(status=204)
	elif bound_up_lat is '':
		return HttpResponse(status=204)
	elif bound_down_lat is '':
		return HttpResponse(status=204)
	elif radius is '':
		return HttpResponse(status=204)
	else:
		center_lng = Decimal(center_lng)
		center_lat = Decimal(center_lat)

		boubd_left_lng = Decimal(boubd_left_lng)
		bound_right_lng = Decimal(bound_right_lng)
		bound_up_lat = Decimal(bound_up_lat)
		bound_down_lat = Decimal(bound_down_lat)

		# convert meter to kilometer
		radius = Decimal(radius) /1000

		first_array = []
		second_array = []
		third_array = []

		# Calculate First Array
		count = 0
		turn_time = 1
		go_time = 1
		has_go = 0
		turn = ['left', 'up', 'right', 'down']

		pre_lng = center_lng
		pre_lat = center_lat

		while isBound(pre_lng, pre_lat, boubd_left_lng, bound_right_lng, bound_up_lat, bound_down_lat):
			first_array.append({'latitude':pre_lat, 'longitude': pre_lng})

			mod = turn_time % 4
			if turn[mod] is 'left':
				dx = -radius
				dy = 0.0
			elif turn[mod] is 'up':
				dx = 0.0
				dy = radius
			elif turn[mod] is 'right':
				dx = radius
				dy = 0.0
			elif turn[mod] is 'down':
				dx = 0.0
				dy = -radius
  
			new_lat, new_lng = calnewlnglat(pre_lat, pre_lng, dx, dy)
			pre_lat = new_lat
			pre_lng = new_lng
			has_go += 1
			if has_go == go_time:
				if (count != 0) and (turn_time % 2 == 0):
					go_time += 1
				has_go = 0
				turn_time += 1
			count += 1


		# Calculate Secondary Array
		count = 0
		turn_time = 1
		go_time = 1
		has_go = 0
		turn = ['right', 'down', 'left', 'up' ]

		pre_lng = (first_array[0]['longitude'] + first_array[2]['longitude'])/2
		pre_lat = (first_array[0]['latitude'] + first_array[2]['latitude'])/2

		while isBound(pre_lng, pre_lat, boubd_left_lng, bound_right_lng, bound_up_lat, bound_down_lat):
			second_array.append({'latitude':pre_lat, 'longitude': pre_lng})

			mod = turn_time % 4
			if turn[mod] is 'right':
				dx = radius
				dy = 0.0
			elif turn[mod] is 'down':
				dx = 0.0
				dy = -radius
			elif turn[mod] is 'left':
				dx = -radius
				dy = 0.0
			elif turn[mod] is 'up':
				dx = 0.0
				dy = radius
  
			new_lat, new_lng = calnewlnglat(pre_lat, pre_lng, dx, dy)
			pre_lat = new_lat
			pre_lng = new_lng
			has_go += 1
			if has_go == go_time:
				if (count != 0) and (turn_time % 2 == 0):
					go_time += 1
				has_go = 0
				turn_time += 1
			count += 1

		# Calculate Third Array
		count = 0
		turn_time = 1
		go_time = 1
		has_go = 0
		turn = ['down', 'left', 'up', 'right']

		pre_lng = (first_array[0]['longitude'] + first_array[1]['longitude'])/2
		pre_lat = (first_array[0]['latitude'] + first_array[1]['latitude'])/2

		while isBound(pre_lng, pre_lat, boubd_left_lng, bound_right_lng, bound_up_lat, bound_down_lat):
			third_array.append({'latitude':pre_lat, 'longitude': pre_lng})

			mod = turn_time % 4
			if turn[mod] is 'down':
				dx = 0.0
				dy = -radius
			elif turn[mod] is 'left':
				dx = -radius
				dy = 0.0
			elif turn[mod] is 'up':
				dx = 0.0
				dy = radius
			elif turn[mod] is 'right':
				dx = radius
				dy = 0.0
  
			new_lat, new_lng = calnewlnglat(pre_lat, pre_lng, dx, dy)
			pre_lat = new_lat
			pre_lng = new_lng
			has_go += 1
			if has_go == go_time:
				if (count != 0) and (turn_time % 2 == 0):
					go_time += 1
				has_go = 0
				turn_time += 1
			count += 1
		
		# meter, km to meter
		radius *= 1000
		content = {
			'center':{
				'latitude':center_lat,
				'longitude':center_lng
			},
			'bound':{
				'bound_down_lat':bound_down_lat,
				'bound_up_lat':bound_up_lat,
				'bound_right_lng':bound_right_lng,
				'boubd_left_lng':boubd_left_lng
			},
			'first':first_array, 
			'second':second_array, 
			'third':third_array, 
			'r':radius
		}
		return HttpResponse(json.dumps(content, default=decimal_default))