#!/usr/bin/python


import csv
import json
import time
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer
from alchemyapi import AlchemyAPI
import requests
from DBspotlight import annotate
from assert_annotation import annotate_with_offset_and_type,annotate_without_offset_and_type,annotate_without_offset,annotate_with_offset


def get_enrichment(prog_uri,text,rdf_graph,out):
	sentences = text.split('.') # split text to annotate in sentences as Spotlight works better with shorter pieces of text
	for sentence in sentences:
		response = annotate(sentence)
		response2graph(prog_uri,response,rdf_graph,out)
	
def response2graph(prog_uri,response,rdf_graph,out):

	
	for resource in response['Resources']:

		rdf_graph = annotate_with_offset_and_type(prog_uri,[resource['@URI']],resource['@types'].split(','),'https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight',{'percentageOfSecondRank':resource['@percentageOfSecondRank'],'similarityScore':resource['@similarityScore'],'support':resource['@support']},start,end,rdf_graph)
		'''
		ann_id = BNode()
		rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id,oa['hasBody'],URIRef(resource['@URI'])))
		rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))
		target_id = BNode()
		rdf_graph.add((ann_id,oa['hasTarget'],target_id))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))

		for type in resource['@types'].split(','):
			rdf_graph.add((URIRef(resource['@URI']),rdf['type'],Literal(type)))

		start = int(resource['@offset'])
		length= len(resource['@surfaceForm'])
		end = start+length
		selector_id = BNode()
		rdf_graph.add((target_id,oa['hasSelector'],selector_id))
		rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
		rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
		rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))

		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(resource['@percentageOfSecondRank'],datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))

		ann_id3 = BNode()
		rdf_graph.add((ann_id3,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id3,oa['hasBody'],Literal('percentageOfSecondRank')))
		rdf_graph.add((ann_id3,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id3,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))


		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(resource['@similarityScore'],datatype=XSD.float)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))

		ann_id5 = BNode()
		rdf_graph.add((ann_id5,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id5,oa['hasBody'],Literal('similarityScore')))
		rdf_graph.add((ann_id5,oa['hasTarget'],ann_id4))
		rdf_graph.add((ann_id5,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))

		ann_id6 = BNode()
		rdf_graph.add((ann_id6,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id6,oa['hasBody'],Literal(resource['@support'],datatype=XSD.integer)))
		rdf_graph.add((ann_id6,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id6,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))

		ann_id7 = BNode()
		rdf_graph.add((ann_id7,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id7,oa['hasBody'],Literal('support')))
		rdf_graph.add((ann_id7,oa['hasTarget'],ann_id6))
		rdf_graph.add((ann_id7,prov['wasGeneratedBy'],URIRef('https://en.wikipedia.org/wiki/DBpedia#DBpedia_Spotlight')))
		'''
	
		
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/DbpediaSpotlight_Enrichment/BBC/synopsis_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'

rdf_graph = Graph()
i = 1
file = 1
max = 1600

missing = open('../Enrichment/DbpediaSpotlight_Enrichment/BBC/missing.csv','w')

'''
with open("../Enrichment/DbpediaSpotlight_Enrichment/BBC/missing.csv", 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    pids = list(reader)

'''

cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	') #read csv file synopsis, pid

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
