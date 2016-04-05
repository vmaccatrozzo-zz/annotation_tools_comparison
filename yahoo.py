import urllib2, urllib, json


def annotate(text):
	
	baseurl = "https://query.yahooapis.com/v1/public/yql?"
	
	yql_query = "select * from contentanalysis.analyze where text=\'"+text+"\'"
	yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&diagnostics=true&format=json"
	
	print yql_url
	result = urllib2.urlopen(yql_url).read()
	return(json.loads(result))

