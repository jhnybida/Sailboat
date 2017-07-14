from __future__ import unicode_literals

import pandas as pd

from retrying import retry
import requests
from bs4 import BeautifulSoup

import datetime

@retry(stop_max_attempt_number=5)
def get_page(i):
	# get the html and try 5 times if need be
    return requests.get('http://sailboatdata.com/viewrecord.asp?class_id='+str(i))

def get_data(i):
	# scrape the data from SailBoatData.com page with index i and return in dict
    
    page = get_page(i)
    soup = BeautifulSoup(page.text.replace('<sup>2</sup>',''), "lxml") # <sup> is for superscript, extra tags are a pain

    # all relevant data has td height=25 beginning with Hull Type
    tags = soup.select('table tr td[height="25"] font b') 
    try:
        first = [t.string.encode('ascii', 'ignore').decode('ascii') for t in tags if t.string].index('Hull Type:')
    except:
    	return dict()

    pairs = [(t.string.strip(),t.find_next('td').string.encode('ascii', 'ignore').decode('ascii').strip()) for t in tags[first:] if t.find_next('td').string]
    data = dict(pairs)
    data.update({'Name:' : soup.title.string.encode('ascii', 'ignore').decode('ascii').strip()})
    return data

def get_all_data():
	# run through all html indices, put in a dataframe and write to a csv file

    data = [get_data(i) for i in range(1,8824)]  # last is 8823
    df = pd.DataFrame(data)

    # output to file
    file_name = 'SBD_%s.csv' % str(datetime.datetime.now()) 
    df.to_csv(file_name, index=False)

    return file_name

def clean_data(file_name):
	df = pd.read_csv(file_name)
	# remove units and other junk
	for s in ['Ballast:','Displacement:']:
	    df[s] = df[s].str.split('/').str[0].str.replace('lbs.|,','').str.strip()
	    df[s] = df[s].astype(float)
	for s in ['Beam:','Draft (max.)','Draft (min.)','E:','EY:','I(IG):','ISP:','J:','LOA:','LWL:','Mast Height from DWL:','P:','PY:','SPL/TPS:']:
	    df[s] = df[s].astype(str).str.split('/').str[0].str.replace("'|,",'').str.strip()
	    df[s] = df[s].astype(float)
	for s in ['Listed SA:','SA(Fore.):','Sail Area (100% fore+main triangles):','SPL/TPS:']:
	    df[s] = df[s].astype(str).str.split('/').str[0].str.replace("ft|,",'').str.strip()
	    df[s] = df[s].astype(float)
	for s in ['Water:','Fuel:']:
	    df[s] = df[s].str.split('/').str[0].str.replace('gals.|,','').str.strip()
	    df[s] = df[s].astype(float)
	for s in ['Bal./Disp.:']:
	    df[s] = df[s].str.replace('%|,','').str.strip()
	    df[s] = df[s].astype(float)
	for s in ['Name:']:
	    df[s] = df[s].str.replace('sailboat specifications and details on sailboatdata.com','').str.strip()
	# rename the columns
	newcols = ['NumBuilt','BallastType','BallastDisp','Ballast','Beam','Builder','Construction','Designer','Displacement','MaxDraft','MinDraft','E','EY','FirstBuilt','Fuel','HP','HullType','I','ISP','J','LOA','LWL','LastBuilt','ListedSA','EngineMake','MastHeight','EngineModel','Name','P','PY','RigType','SAFore','SPLTPS','SA','SADisp1','SADisp2','FuelType','Water']
	df.columns = newcols
	# drop Null rows
	df = df.drop(df[df['Name'].isnull()].index)
	df = df.set_index('Name')
	# add other ratios
	df['DispLen'] = df.Displacement/2240/(0.01*df.LWL)**3
	df['MotionComfort'] = df.Displacement/(0.65 * (0.7 df.LWL + 0.3 df.LOA) x df.Beam**1.333)
	df['CapsizeScreening'] = df.Beam/(Displ/64)**0.333
	# output to file
	df.to_csv('C'+file_name)
	print(df)

if __name__=='__main__':
    #file_name = get_all_data()
    clean_data('SBD_2017-06-28 07:25:24.213783.csv')
