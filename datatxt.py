import requests


def annotate(text):
	
	#https://api.dandelion.eu/datatxt/nex/v1/? text=The%20doctor%20says%20an%20apple%20is%20better%20than%20an%20orange&include=types%2Cabstract%2Ccategories&$app_id=YOUR_APP_ID&$app_key=YOUR_APP_KEY
	header = {'Accept': 'application/json'}
	
	app_id = "YOUR API ID HERE"
	app_key = "YOUR API KEY HERE"
	url ='https://api.dandelion.eu/datatxt/nex/v1/?include=types%2Clod&$app_id='+app_id'+&$app_key='+app_key+'&text='+text
	
	r = requests.get(url, headers=header)
	try:
		return r.json()
	except:
		pass