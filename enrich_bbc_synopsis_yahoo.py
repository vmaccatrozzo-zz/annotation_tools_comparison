import csv
import time
from nltk.tokenize import word_tokenize
import datetime
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from yahoo import annotate
from assert_annotation import annotate_with_offset_and_type,annotate_without_offset_and_type,annotate_without_offset,annotate_with_offset

skos =	Namespace('http://www.w3.org/2004/02/skos/core#')
lt = Namespace('http://www.LibraryThing.com/Book/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')
prov = Namespace('http://www.w3.org/ns/prov#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
dcterms = Namespace('http://purl.org/dc/terms/')


def get_enrichment(programme_uri,synopsis,rdf_graph):
 	
	response = annotate(synopsis)
	response2graph(programme_uri,response, rdf_graph)
	
def response2graph(programme_uri,response, rdf_graph):
	
	try:
		for entity in response['query']['results']['entities']['entity']:
			rdf_graph = annotate_with_offset(programme_uri,[entity['text']['content']],'http://www.yahoo.com/',{'score':entity['score']},entity['text']['start'],entity['text']['end'],rdf_graph)
			'''
			ann_id = BNode()
			rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id,oa['hasBody'],Literal(entity['text']['content'])))
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
			target_id = BNode()
			rdf_graph.add((ann_id,oa['hasTarget'],target_id))
			rdf_graph.add((target_id,oa['hasSource'],URIRef(programme_uri)))
			rdf_graph.add((target_id,oa['exact'],Literal(entity['text']['content'])))
			selector_id=BNode()
			rdf_graph.add((target_id,oa['hasSelector'],selector_id))
			rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
			rdf_graph.add((selector_id,oa['start'],Literal(entity['text']['start'],datatype=XSD.integer)))
			rdf_graph.add((selector_id,oa['end'],Literal(entity['text']['end'],datatype=XSD.integer)))
			ann_id2 = BNode()
			rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id2,oa['hasBody'],Literal(entity['score'],datatype=XSD.float)))
			rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
			ann_id4 = BNode()
			rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id4,oa['hasBody'],Literal('score')))
			rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
			rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
			'''
	except:
	
	#print response['query']['results']['entities']['entity']['text']['content']
	#for entity in response['query']['results']['entities']['entity']['text']['content']:
		#print response
		if response['query']['results']['entities'] is not None:
			rdf_graph = annotate_with_offset(programme_uri,[response['query']['results']['entities']['entity']['text']['content']],'http://www.yahoo.com/',{'score':response['query']['results']['entities']['entity']['score']},response['query']['results']['entities']['entity']['text']['start'],response['query']['results']['entities']['entity']['text']['end'],rdf_graph)
			'''
			ann_id = BNode()
			rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id,oa['hasBody'],Literal(response['query']['results']['entities']['entity']['text']['content'])))
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
			target_id = BNode()
			rdf_graph.add((ann_id,oa['hasTarget'],target_id))
			rdf_graph.add((target_id,oa['hasSource'],URIRef(programme_uri)))
			rdf_graph.add((target_id,oa['exact'],Literal(response['query']['results']['entities']['entity']['text']['content'])))
			selector_id=BNode()
			rdf_graph.add((target_id,oa['hasSelector'],selector_id))
			rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
			rdf_graph.add((selector_id,oa['start'],Literal(response['query']['results']['entities']['entity']['text']['start'],datatype=XSD.integer)))
			rdf_graph.add((selector_id,oa['end'],Literal(response['query']['results']['entities']['entity']['text']['end'],datatype=XSD.integer)))
			ann_id2 = BNode()
			rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id2,oa['hasBody'],Literal(response['query']['results']['entities']['entity']['score'],datatype=XSD.float)))
			rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
			ann_id4 = BNode()
			rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id4,oa['hasBody'],Literal('score')))
			rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
			rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('http://www.yahoo.com/')))
		'''
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/Yahoo_Enrichment/BBC/synopses_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'


rdf_graph = Graph()
i = 1
file = 1
max = 1600

missing = open('../Enrichment/Yahoo_Enrichment/BBC/missing.csv','w')

'''
with open("../Enrichment/Yahoo_Enrichment/BBC/missing.csv", 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    pids = list(reader)
'''
cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')

for programme in cr:   
	pid = programme[1]
	#if pid in pids[0]:
	synopsis = unicode(programme[0],errors='replace')
	prog_uri = 'http://www.bbc.co.uk/programmes/'+pid+'#programme'

	print pid

	if i == max:
		i = 1
		write_graph(file,rdf_graph)
		rdf_graph = Graph()
		file = file + 1

	try:
		get_enrichment(prog_uri,synopsis,rdf_graph)
	except:
		missing.write(pid+',')
		continue	

	i = i + 1
	

if i > 0:	
	write_graph(file,rdf_graph)


