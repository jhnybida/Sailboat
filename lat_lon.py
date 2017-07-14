import pandas as pd
from time import sleep
from geopy.geocoders import Nominatim
from retrying import retry
import cPickle as pickle

def find_lat_lon(pdseries):

	geolocator = Nominatim()
	unique_places = pdseries.unique()
	lat_lon_dict = dict()

	@retry(stop_max_attempt_number=50,wait_random_min=10000, wait_random_max=200000)
	def get_loc(place):
		return geolocator.geocode(place, timeout = None)

	print(len(unique_places)) # AIzaSyCtMsUQOFaS_lF9XF-hny1uLuh4kvKQe7Q
	for i,place in enumerate(unique_places):
		location = get_loc(place)
		if location:
			lat_lon_dict[place] = (location.longitude,location.latitude)
		sleep(1)
		print(i)

	with open('lat_lon_dict.txt', 'w') as file:
		file.write(pickle.dumps(lat_lon_dict))

	def get_lat_lon(place):
		if place in lat_lon_dict:
			return lat_lon_dict[place]
		else:
			return None

	return pdseries.apply(get_lat_lon)


if __name__ == '__main__':

	df = pd.read_csv('JOINED.csv',low_memory=False)

	df['LatLon'] = find_lat_lon(df['Location'])

	df.to_csv('LATLON.csv',index=False)


