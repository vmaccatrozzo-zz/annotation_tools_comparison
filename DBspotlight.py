import requests


def annotate(text):
	
	
	header = {'Accept': 'application/json'}
	url ='http://spotlight.sztaki.hu:2222/rest/annotate?text='+text+'&confidence=0.2&support=20'
	r = requests.get(url, headers=header)
	try:
		return r.json()
	except:
		pass