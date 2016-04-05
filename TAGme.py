import requests


def annotate(text):
	
	KEY = "YOUR KEY HERE"
	header = {'Accept': 'application/json'}
	url ='http://tagme.di.unipi.it/tag?text='+text+'&key='+KEY+'&include_categories=true'
	r = requests.get(url, headers=header)
	try:
		return r.json()
	except:
		pass