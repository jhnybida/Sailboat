from __future__ import unicode_literals
import os

import pandas as pd

import requests
from bs4 import BeautifulSoup
import urllib

from datetime import datetime, timedelta

hmid = {'all' : 0,					# material
		'aluminum' : 100,		
		'composite' : 101,
		'fiberglass' : 102,
		'steel' : 103,
		'wood' : 104,
		'other' : 105,
		'hypalon' : 106,
		'pvc' : 107,
		'ferro-cement' : 108
		}

types = ['','+Antique+and+Classic', '+Barge', '+Catamaran', '+Center+Cockpit', '+Commercial+Boat',  #classification
		 '+Cruiser','+Cruiser/Racer','+Cutter','+Daysailer','+Deck+Saloon', 
		 '+Ketch','+Motorsailer','+Multi-Hull','+Pilothouse', '+Racing+Sailboat', 
		 '+Schooner', '+Sloop', '+Trimaran', '+Yawl', '+Other']

enid = {-1 : 0,		# all
		 1 : 100, 			# number of engines
		 2 : 101,
		 0 : 103
		}

ftid = {'all' : 0,			# fuel type
		'gas' : 100,
		'diesel' : 101,
		'other' : 102
		}


def get_urls(days_since_posted = -1, 	# number of days since ad was posted
			 material = 'all', 			# hmid
			 classification = '', 		# types
			 numEngines = -1, 			# 0,1,2
			 isnew = '', 				# 'true' or 'false' or ''
			 fueltype = 'all' 			# all, gas, diesel, other
			 ):
	
	# pbsint: all ads posed since date in ms from 1970
	current_date_ms = int(datetime.now().date().strftime('%s'))*1000
	day_in_ms = 86400000
	pbsint = current_date_ms - days_since_posted*day_in_ms
	if days_since_posted == -1:  # for all time
		pbsint = -1

	args = {"searchtype" : "advancedsearch", 
			"Ntk" : "boatsEN",
			"type" : "(Sail)" + classification,
			"hmid" : hmid[material],
			"sm" : 3,
			"enid" : enid[numEngines],
			"cit" : "true",
			"currencyid" : 100,
			"luom" : 126,
			"is" : isnew,
			"boatsAddedSelected" : 3,
			"ftid" : ftid[fueltype],
			"pbsint" : pbsint,
			"ps" : 10,					# number of ads per page
			"slim" : "quick",
			"No" : 0,		
			'fracts' : 1				# exclude fractional boats
			}

	url = "http://www.yachtworld.com/core/listing/cache/searchResults.jsp?{}".format(urllib.urlencode(args))

	first_page = requests.get(url)

	soup = BeautifulSoup(first_page.text, "lxml") 

	try:
		iteminfo = soup.select('span[id="searchResultsCount"] b')[0].string
	except:
		print('cant get urls')
		return []

	num_boats = int(iteminfo.split(' ')[-1].replace(',',''))
	
	ads_per_page = 500

	args['ps'] = ads_per_page				# set number of ads per page to 500
	num_pages = num_boats//ads_per_page+1	

	url_list = []
	for i in range(num_pages):
		args['No'] = ads_per_page*i
		url = "http://www.yachtworld.com/core/listing/cache/searchResults.jsp?{}".format(urllib.urlencode(args))
		url_list.append(url)

	return url_list

def get_data(url):
	# scrape the data from a Yachtworld url and return in a dict
	
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "lxml") 

	# get all listing tags for the page
	tags = soup.select('div[class="listing-container"]') 

	#create list of dicts for each listing
	dict_list = []
	for t in tags:
		ID = t.get('data-reporting-impression-product-id')
		listing_type = t.get('data-reporting-impression-listing-type')
		href = t.select('a')[0].get('href')
		mm = t.select('div[class="make-model"] a')[0].text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n','')
		mm = ' '.join(mm.split())
		price = t.select('div[class="price"]')[0].text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n','')
		location = t.select('div[class="location"]')[0].text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n','')
		location = ' '.join(location.split())
		broker = t.select('div[class="broker"]')[0].text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n','')
		description = t.select('div[class="description"]')[0].text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n','')

		tdict = {'ID':ID,'ListingType':listing_type,'href':href,'MakeModel':mm,'Price':price,'Location':location,'Broker':broker,'Description':description}

		dict_list.append(tdict)

	return dict_list

def create_database(dsp): # scrapes all data from YW
	
	# get urls for most general data
	urls = get_urls(days_since_posted=dsp)

	# save data in list of dicts
	data = []
	for url in urls:
		dl = get_data(url)
		data.extend(dl)

	# make dataframe
	df = pd.DataFrame(data)

	# add other columns
	df = add_PostedAfter(df,dsp)
	df = add_Material(df,dsp)
	df = add_Types(df,dsp)
	df = add_FuelType(df,dsp)
	df = add_NumEngines(df,dsp)

	df = clean_data(df)

	return df

# def update_database(df_old, dsp):

# 	df_new = create_database(dsp)

# 	df_cat = pd.concat([df_old,df_new])

# 	return df_cat.sort_values('PostedAfter', ascending=False).drop_duplicates(['Mt'])

def add_PostedAfter(df,dsp):

	df['PostedAfter'] = (datetime.now() - timedelta(days=3650)).date()

	if dsp == -1:
		dsp = 3650

	day_list = [x for x in range(1,64,7)+range(64,1000,30)+range(1000,3650,300) if x < dsp]

	for num in day_list:
		numdate = (datetime.now() - timedelta(days=num)).date()
		urls = get_urls(days_since_posted = num)
		for url in urls:
			dft = pd.DataFrame(get_data(url))
			if not dft.empty:
				df.loc[df.ID.isin(dft.ID) & (df.PostedAfter < numdate),'PostedAfter'] = numdate 
		print(num)
	return df

def add_Material(df,dsp):

	df['Material'] = ''

	for hm in hmid:
		if hm != 'all':
			urls = get_urls(days_since_posted = dsp, material = hm)
			for url in urls:
				dft = pd.DataFrame(get_data(url))
				if not dft.empty:
					df.loc[df.ID.isin(dft.ID),'Material'] = hm
			print(hm)
	return df

def add_Types(df,dsp):

	for t in types[1:]:
		df[t] = 0
		urls = get_urls(days_since_posted = dsp, classification = t)
		for url in urls:
			dft = pd.DataFrame(get_data(url))
			if not dft.empty:
				df.loc[df.ID.isin(dft.ID),t] = 1
		print(t)
	return df

def add_FuelType(df,dsp):

	df['FuelType'] = ''

	for ft in ftid:
		if ft != 'all':
			urls = get_urls(days_since_posted = dsp, fueltype = ft)
			for url in urls:
				dft = pd.DataFrame(get_data(url))
				if not dft.empty:
					df.loc[df.ID.isin(dft.ID),'FuelType'] = ft
			print(ft)
	return df

def add_NumEngines(df,dsp):

	df['NumEngines'] = ''

	for en in enid:
		if en != -1:
			urls = get_urls(days_since_posted = dsp, numEngines = en)
			for url in urls:
				dft = pd.DataFrame(get_data(url))
				if not dft.empty:
					df.loc[df.ID.isin(dft.ID),'NumEngines'] = en
			print(en)
	return df


def clean_data(df):

	# remove units and other junk
	df['Length'] = df['MakeModel'].str.split().str[0].str.replace('ft','').astype(int)
	df['Year'] = df['MakeModel'].str.split().str[1].astype(int)
	df['MakeModel'] = df['MakeModel'].str.split().str[2:].str.join(' ')
	df['Price'] = df['Price'].str.replace('US','').str.replace('$','').str.replace(',','')
	df['href'] = df['href'].str.strip()

	# drop Null rows
	df = df.drop(df[df['ID'].isnull()].index)
	df = df.set_index('ID')

	#df.Price = df.Price.str.replace('Call','').str.strip()
	df = df[df['Price'].astype(str).str.isdigit()]
	df = df[df['Price'].astype(int) != 1 ]
	df.Price = df.Price.astype(int)

	df.Length = df.Length.astype(int)
	df.Year = df.Year.astype(int)

	df.columns = [x.replace('+','').replace('/','') for x in df.columns]

	return df

def output_to_file(df):

	file_name = 'YW.csv'  
	df.to_csv(file_name)

	directory = './data'
	file_name = directory + '/YW_%s.csv' % str(datetime.now())
	if not os.path.exists(directory):
		os.makedirs(directory)
	df.to_csv(file_name)



if __name__=='__main__':
	df = create_database(dsp = -1)
	output_to_file(df)