#!/usr/bin/python

import csv
import json
import time
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from TAGme import annotate
from assert_annotation import annotate_with_offset_and_type,annotate_without_offset_and_type,annotate_without_offset,annotate_with_offset


def get_enrichment(prog_uri,text,rdf_graph):
	
	response = annotate(text)
	
	response2graph(prog_uri,text,response,rdf_graph)
	
	
	
def response2graph(prog_uri,synopsis,response, rdf_graph):
		
	
	for annotation in response['annotations']:
		end = annotation['end']
		start = annotation['end']
		label = annotation['spot']
		relevance = annotation['rho']
		
		try:
			title = annotation['title']
			dbpedia_uri='http://dbpedia.org/resource/'+title.replace(' ','_')
			rdf_graph = annotate_with_offset(prog_uri,[title,dbpedia_uri],'http://tagme.di.unipi.it/',{},start,end,rdf_graph)
		except:
			title = label
			rdf_graph = annotate_with_offset(prog_uri,[title],'http://tagme.di.unipi.it/',{'relevance' : relevance},start,end,rdf_graph)
		
		'''
		ann_id = BNode()
		rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id,oa['hasBody'],Literal(title)))
		rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://tagme.di.unipi.it/')))
		target_id = BNode()
		rdf_graph.add((ann_id,oa['hasTarget'],target_id))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(dbpedia_uri)))
		rdf_graph.add((target_id,oa['exact'],Literal(label)))
		selector_id=BNode()
		rdf_graph.add((target_id,oa['hasSelector'],selector_id))
		rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
		rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
		rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(relevance,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://tagme.di.unipi.it/')))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal('relevance')))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('http://tagme.di.unipi.it/')))
		'''
			
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/TAGme_Enrichment/BBC/synopsis_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'

rdf_graph = Graph()
file = 1
max = 1600
i = 1	

missing = open('../Enrichment/TAGme_Enrichment/BBC/missing_pids.csv','w')
cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')

#with open("../Enrichment/TAGme_Enrichment/BBC/first_missing_pids.csv", 'rb') as f:
#    reader = csv.reader(f)
#    pids1 = list(reader)
   
for programme in cr:   
	pid = programme[1]
	#if pid in pids1[0]:
		synopsis = unicode(programme[0],errors='replace')
		prog_uri = 'http://www.bbc.co.uk/programmes/'+pid+'#programme'
			
		print pid
		if i == max:
			i=1
			write_graph(file,rdf_graph)
			rdf_graph = Graph()
			file = file + 1
	
		try:
			get_enrichment(prog_uri,synopsis,rdf_graph)
		except:
			missing.write(pid+',')
		
		i = i + 1
	 
	
if i > 0:	
	write_graph(file,rdf_graph)