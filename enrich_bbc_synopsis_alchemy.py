#!/usr/bin/python

import csv
import json
import time
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from alchemyapi import AlchemyAPI
from assert_annotation import annotate_with_offset,annotate_without_offset
alchemyapi = AlchemyAPI()

skos =	Namespace('http://www.w3.org/2004/02/skos/core#')
lt = Namespace('http://www.LibraryThing.com/Book/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')
prov = Namespace('http://www.w3.org/ns/prov#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
dcterms = Namespace('http://purl.org/dc/terms/')

def get_enrichment(prog_uri,text,rdf_graph):
	
	response = alchemyapi.combined('text', text,{'linkedData':1,'showSourceText':1})
	if response['status'] == 'OK':
		response2graph(prog_uri,text,response,rdf_graph)
	else:
		print('Error in combined call: ', response['statusInfo'])
	
def response2graph(prog_uri,synopsis,response, rdf_graph):
	for uri in prog_uri:
		for keyword in response['keywords']:
			try:
				start = synopsis.index(keyword['text'])
				end = start+len(keyword['text'])
		
				rdf_graph = annotate_with_offset(uri,[keyword['text']],'http://www.alchemyapi.com/',{'relevance':keyword['relevance']},start,end,rdf_graph)
				
			except:
				rdf_graph = annotate_without_offset(uri,[keyword['text']],'http://www.alchemyapi.com/',{'relevance':keyword['relevance']},rdf_graph)
			'''
			ann_id = BNode()
			rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id,oa['hasBody'],Literal(keyword['text'])))
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			target_id = BNode()
			rdf_graph.add((ann_id,oa['hasTarget'],target_id))
			rdf_graph.add((target_id,oa['hasSource'],URIRef(uri)))
			ann_id2 = BNode()
			rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id2,oa['hasBody'],Literal(keyword['relevance'],datatype=XSD.float)))
			rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
		
			try:
				start = synopsis.index(keyword['text'])
				end = start+len(keyword['text'])
				selector_id=BNode()
				rdf_graph.add((target_id,oa['hasSelector'],selector_id))
				rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
				rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
				rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
			except:
				continue
			'''
		annotations = []
		for concept in response['concepts']:
			annotations.append(concept['text']
			try:
				annotations.append(concept['dbpedia'])
			except:
				continue
			try:
				annotations.append(concept['yago'])
			except:
				continue
			try:
				annotations.append(concept['freebase'])
			except:
				continue
				
			rdf_graph = annotate_without_offset(uri,annotations,'http://www.alchemyapi.com/',{},rdf_graph)
			'''
			ann_id = BNode()
			rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
			try:
				rdf_graph.add((ann_id,oa['hasBody'],URIRef(concept['dbpedia'])))
			except:
				pass
			try:
				rdf_graph.add((ann_id,oa['hasBody'],URIRef(concept['yago'])))
			except:
				pass
			try:
				rdf_graph.add((ann_id,oa['hasBody'],URIRef(concept['freebase'])))
			except:
				pass
			rdf_graph.add((ann_id,oa['hasBody'],Literal(concept['text'])))
			target_id = BNode()
			rdf_graph.add((ann_id,oa['hasTarget'],target_id))
			rdf_graph.add((target_id,oa['hasSource'],URIRef(uri)))		
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			ann_id2 = BNode()
			rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id2,oa['hasBody'],Literal(concept['relevance'],datatype=XSD.float)))
			rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			'''
		for entity in response['entities']:
			
			
			try:
				start = synopsis.index(entity['text'])
				end = start+len(entity['text'])
		
				rdf_graph = annotate_with_offset(uri,[entity['text']],'http://www.alchemyapi.com/',{'relevance':entity['relevance']},start,end,rdf_graph)
				
			except:
				rdf_graph = annotate_without_offset(uri,[entity['text']],'http://www.alchemyapi.com/',{'relevance':entity['relevance']},rdf_graph)
			'''
			ann_id = BNode()
			rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id,oa['hasBody'],Literal(entity['text'])))
			target_id = BNode()
			rdf_graph.add((ann_id,oa['hasTarget'],target_id))
			rdf_graph.add((target_id,oa['hasSource'],URIRef(uri)))
			rdf_graph.add((ann_id,rdf['type'],Literal(entity['type'])))
		
			
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			ann_id2 = BNode()
			rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id2,oa['hasBody'],Literal(entity['relevance'],datatype=XSD.float)))
			rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			ann_id3 = BNode()
			rdf_graph.add((ann_id3,rdf['type'],oa['Annotation']))
			rdf_graph.add((ann_id3,oa['hasBody'],Literal(entity['type'])))
			rdf_graph.add((ann_id3,oa['hasTarget'],ann_id))
			rdf_graph.add((ann_id3,prov['wasGeneratedBy'],URIRef('http://www.alchemyapi.com/')))
			try:
				start = synopsis.index(entity['text'])
				end = start+len(entity['text'])
				selector_id = BNode()
				rdf_graph.add((target_id,oa['hasSelector'],selector_id))
				rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
				rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
				rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
			except:
				continue
			'''
		
		

def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/AlchemyAPI_Enrichment/BBC/synopsis_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'

rdf_graph = Graph()
rdf_graph = Graph()
file = 1
max = 1000
i = 1	

cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')
missing = open('../Enrichment/AlchemyAPI_Enrichment/BBC/missing.csv','w')

'''
with open("../Enrichment/AlchemyAPI_Enrichment/BBC/missing.csv", 'rb') as f:
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
