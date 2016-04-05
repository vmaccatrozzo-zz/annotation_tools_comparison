import textrazor
import csv
import time
from nltk.tokenize import word_tokenize
import datetime
from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer

skos =	Namespace('http://www.w3.org/2004/02/skos/core#')
lt = Namespace('http://www.LibraryThing.com/Book/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')
prov = Namespace('http://www.w3.org/ns/prov#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
dcterms = Namespace('http://purl.org/dc/terms/')

textrazor.api_key = "YOUR API KEY HERE"

from assert_annotation import annotate_with_offset_and_type,annotate_without_offset_and_type,annotate_without_offset,annotate_with_offset



def get_enrichment(book_uri,synopsis,rdf_graph):
 	
	client = textrazor.TextRazor(extractors=["entities", "topics"])
	response = client.analyze(synopsis)
	
	if response.ok == True:
		response2graph(book_uri,response,synopsis,rdf_graph)
	else:
		print('Error: ', response.error)
		
def response2graph(prog_uri,response,synopsis, rdf_graph):

	
	for topic in response.topics():	
		annotations=[]
		annotations.append(topic.label)
		
		'''
		ann_id = BNode()
		rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id,oa['hasBody'],Literal(topic.label)))
		rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		
		target_id = BNode()
		rdf_graph.add((ann_id,oa['hasTarget'],target_id))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(book_uri)))
		'''
		if topic.wikipedia_link is not None:
			dbpedia_uri = (topic.wikipedia_link).replace('en.wikipedia.org/wiki','dbpedia.org/resource')
			annotations.append(dbpedia_uri)
			#rdf_graph.add((ann_id,oa['hasBody'],URIRef(dbpedia_uri)))
		rdf_graph = annotate_without_offset(prog_uri,annotations,'https://www.textrazor.com/',{'score':topic.score},rdf_graph)
		'''
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(topic.score,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal('relevance')))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		'''
	for entity in response.entities():
		
		annotations=[]
		annotations.append(entity.id)
		start = synopsis.index(entity.matched_text)
		end = start+len(entity.matched_text)
		'''
		ann_id = BNode()
		rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id,oa['hasBody'],Literal(entity.id)))
		
		target_id = BNode()
		rdf_graph.add((ann_id,oa['hasTarget'],target_id))
		rdf_graph.add((target_id,oa['hasSource'],URIRef(book_uri)))
		selector_id=BNode()
		rdf_graph.add((target_id,oa['hasSelector'],selector_id))
		rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
		rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
		rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
		
		for type in entity.dbpedia_types:
			rdf_graph.add((ann_id,rdf['type'],Literal(type)))
		'''
		if entity.wikipedia_link is not None:
			dbpedia_uri = (entity.wikipedia_link).replace('en.wikipedia.org/wiki','dbpedia.org/resource')
			annotations.append(dbpedia_uri)
			#rdf_graph.add((ann_id,oa['hasBody'],URIRef(dbpedia_uri)))
		if entity.freebase_id is not None:
			freebase_uri = 'http://www.freebase.com/'+entity.freebase_id
			annotations.append(freebase_uri)
			'''
			rdf_graph.add((ann_id,oa['hasBody'],URIRef(freebase_uri)))
			rdf_graph.add((ann_id,oa['hasTarget'],URIRef(book_uri)))
			rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
			'''
		rdf_graph = annotate_without_offset_and_type(prog_uri,annotations,entity.dbpedia_types,'https://www.textrazor.com/',{'relevance':entity.relevance_score,'confidence':entity.confidence_score},rdf_graph)
		'''
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(entity.relevance_score,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal('relevance')))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		ann_id3 = BNode()
		rdf_graph.add((ann_id3,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id3,oa['hasBody'],Literal(entity.confidence_score)))
		rdf_graph.add((ann_id3,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id3,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		ann_id5 = BNode()
		rdf_graph.add((ann_id5,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id5,oa['hasBody'],Literal('confidence')))
		rdf_graph.add((ann_id5,oa['hasTarget'],ann_id3))
		rdf_graph.add((ann_id5,prov['wasGeneratedBy'],URIRef('https://www.textrazor.com/')))
		'''	
def write_graph(file, rdf_graph):
	print 'writing rdf file'
	file_name = '../Enrichment/TextRazor_Enrichment/BBC/synopses_part'+str(file)+'.rdf' 
	rdf_graph.serialize(file_name, format="xml")
	print 'finished writing rdf file'


rdf_graph = Graph()
i = 1
file = 9
max = 500

missing = open('../Enrichment/TextRazor_Enrichment/BBC/missing.csv','w')

#pids = csv.reader(open("../Enrichment/TextRazor_Enrichment/BBC/first_missing.csv","rb"))
with open("../Enrichment/TextRazor_Enrichment/BBC/pids_done.csv", 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    pids = list(reader)

print pids[0]

cr = csv.reader(open("../data/BBC/BBC_programmes.csv","rb"), delimiter='	')
#print 'sleeping until one am'
#time.sleep(900)
for programme in cr:   
	pid = programme[1]
	if pid not in pids[0]:
		synopsis = unicode(programme[0],errors='replace')
		prog_uri = 'http://www.bbc.co.uk/programmes/'+pid+'#programme'
			
		print pid

		if i == max:
			i = 1
			write_graph(file,rdf_graph)
			rdf_graph = Graph()
			file = file + 1
			now = datetime.datetime.now()
			tomorrowmidnight = now.replace(hour=1, minute=0, second=0, microsecond=0,day = now.day+1)
			print "waiting for the new day..."
			time.sleep((tomorrowmidnight - now).total_seconds()+60)
			print "awake!"
		try:
			get_enrichment(prog_uri,synopsis,rdf_graph)
		except:
			missing.write(pid+',')
			continue	
	
		i = i + 1

if i > 0:	
	write_graph(file,rdf_graph)


