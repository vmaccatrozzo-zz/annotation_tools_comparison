#!/usr/bin/python


import csv
import json
import time
import datetime
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from alchemyapi import AlchemyAPI
import requests
from datatxt import annotate
from assert_annotation import annotate_with_offset,annotate_without_offset

rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')
prov = Namespace('http://www.w3.org/ns/prov#')

def get_enrichment(prog_uri,text,rdf_graph):
		
		response = annotate(text)
		print response
		
		response2graph(prog_uri,response,rdf_graph)
		
		
def response2graph(prog_uri,response,rdf_graph):
	
	for resource in response['annotations']:
	
		rdf_graph = annotate_with_offset(prog_uri,[resource['lod']['dbpedia'],resource['label']],'https://dandelion.eu',{'confidence':resource['confidence']},resource['start'],resource['end'],rdf_graph)
		'''
		ann_id = BNode()
		rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id,oa['hasBody'],URIRef(resource['lod']['dbpedia'])))
		rdf_graph.add((ann_id,oa['hasBody'],Literal(resource['label'])))
		rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('https://dandelion.eu')))
		target_id = BNode()
		rdf_graph.add((ann_id,oa['hasTarget'],target_id))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))

		for type in resource['types']:
			type = str(type).replace('http://dbpedia.org/ontology/','')
			rdf_graph.add((URIRef(resource['lod']['dbpedia']),rdf['type'],Literal(type)))

		selector_id = BNode()
		rdf_graph.add((target_id,oa['hasSelector'],selector_id))
		rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
		rdf_graph.add((selector_id,oa['start'],Literal(resource['start'],datatype=XSD.integer)))
		rdf_graph.add((selector_id,oa['end'],Literal(resource['end'],datatype=XSD.integer)))
	
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(resource['confidence'],datatype=XSD.float)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('https://dandelion.eu')))

		ann_id5 = BNode()
		rdf_graph.add((ann_id5,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id5,oa['hasBody'],Literal('confidence')))
		rdf_graph.add((ann_id5,oa['hasTarget'],ann_id4))
		rdf_graph.add((ann_id5,prov['wasGeneratedBy'],URIRef('https://dandelion.eu')))
		'''
		
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/Datatxt_Enrichment/BBC/synopsis_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'

rdf_graph = Graph()
file = 1
max = 1000
i = 1	

cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')
missing = open('../Enrichment/Datatxt_Enrichment/BBC/missing.csv','w')

'''
with open("../Enrichment/Datatxt_Enrichment/BBC/first_missing.csv", 'rb') as f:
    reader = csv.reader(f)
    pids1 = list(reader)
'''    

for programme in cr:   
	prog_uri = 'http://www.bbc.co.uk/programmes/'+pid+'#programme'	
	print pid
	#if pid in pids1[0]:
	if i == max:
		i = 1
		write_graph(file,rdf_graph)
		rdf_graph = Graph()
		file = file + 1
		now = datetime.datetime.now()
		tomorrowmidnight = now.replace(hour=0, minute=0, second=0, microsecond=0,day = now.day+1)
		print "waiting for the new day..."
		time.sleep((tomorrowmidnight - now).total_seconds()+60)
		print "awake!"
	
	try:
		get_enrichment(prog_uri,synopsis,rdf_graph)
	except:
		missing.write(pid+'\n')
		
	i = i + 1
	
if i > 0:	
	write_graph(file,rdf_graph)
