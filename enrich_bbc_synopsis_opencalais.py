import csv
import time
from nltk.tokenize import word_tokenize
import datetime
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from opencalais import annotate
from assert_annotation import annotate_with_offset_and_type,annotate_without_offset_and_type,annotate_without_offset


rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')



def get_enrichment(programme_uri,synopsis,rdf_graph):
 	
	response = annotate(synopsis)	
	response2graph(programme_uri,response, rdf_graph)
		
def response2graph(programme_uri,response, rdf_graph):
	for elem in response:
		if '_typeGroup' in response[elem].keys():
			if response[elem]['_typeGroup'] == 'socialTag':
				name = response[elem]['name']
				importance = response[elem]['importance']
				
				rdf_graph = annotate_without_offset(programme_uri,[name],'http://www.opencalais.com/',{'importance':importance},rdf_graph)
				'''
				ann_id = BNode()
				rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id,oa['hasBody'],Literal(name)))
				rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				target_id = BNode()
				rdf_graph.add((ann_id,oa['hasTarget'],target_id))
				rdf_graph.add((target_id,oa['hasSource'],URIRef(programme_uri)))
				ann_id2 = BNode()
				rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id2,oa['hasBody'],Literal(importance,datatype=XSD.float)))
				rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
				rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				ann_id4 = BNode()
				rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id4,oa['hasBody'],Literal('importance')))
				rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
				rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				'''
			if response[elem]['_typeGroup'] == 'entities':
				name =  response[elem]['name']
				type = response[elem]['_type']
				for data in response[elem]['instances']:
					start = data['offset']
					exact = data['exact']
					length = data['length']
				end = start + length
				relevance = response[elem]['relevance']
				'''
				ann_id = BNode()
				rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id,rdf['type'],Literal(type)))
				rdf_graph.add((ann_id,oa['hasBody'],Literal(name)))
				rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				target_id = BNode()
				rdf_graph.add((ann_id,oa['hasTarget'],target_id))
				rdf_graph.add((target_id,oa['hasSource'],URIRef(programme_uri)))
				rdf_graph.add((target_id,oa['exact'],Literal(exact)))
				selector_id=BNode()
				rdf_graph.add((target_id,oa['hasSelector'],selector_id))
				rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
				rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
				rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
				ann_id2 = BNode()
				rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id2,oa['hasBody'],Literal(relevance,datatype=XSD.float)))
				rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
				rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				ann_id4 = BNode()
				rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
				rdf_graph.add((ann_id4,oa['hasBody'],Literal('relevance')))
				rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
				rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
				'''
				try:
					confidencelevel = response[elem]['confidencelevel']
					'''
					ann_id3 = BNode()
					rdf_graph.add((ann_id3,rdf['type'],oa['Annotation']))
					rdf_graph.add((ann_id3,oa['hasBody'],Literal(confidencelevel)))
					rdf_graph.add((ann_id3,oa['hasTarget'],ann_id))
					rdf_graph.add((ann_id3,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
					ann_id5 = BNode()
					rdf_graph.add((ann_id5,rdf['type'],oa['Annotation']))
					rdf_graph.add((ann_id5,oa['hasBody'],Literal('confidence')))
					rdf_graph.add((ann_id5,oa['hasTarget'],ann_id3))
					rdf_graph.add((ann_id5,prov['wasGeneratedBy'],URIRef('http://www.opencalais.com/')))
					'''
					rdf_graph = annotate_with_offset_and_type(programme_uri,[name],[type],'http://www.opencalais.com/',{'relevance':relevance,'confidencelevel':confidencelevel},start,end,rdf_graph)
				except:
					rdf_graph = annotate_with_offset_and_type(programme_uri,[name],[type],'http://www.opencalais.com/',{'relevance':relevance},start,end,rdf_graph)
				
				
	
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/OpenCalais_Enrichment/BBC/synopses_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'


rdf_graph = Graph()
i = 1
file = 1
max = 1600

missing = open('../Enrichment/OpenCalais_Enrichment/BBC/missing.csv','w')

'''
with open("../Enrichment/OpenCalais_Enrichment/BBC/missing.csv", 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    pids = list(reader)

'''

cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')

for programme in cr:   
	pid = programme[1]
	#if pid in pids:
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


