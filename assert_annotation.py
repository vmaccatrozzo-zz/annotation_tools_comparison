from rdflib import URIRef,Literal,XSD,BNode,Namespace,plugin
from rdflib.graph import Graph
from rdflib.serializer import Serializer

rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oa = Namespace('http://www.w3.org/ns/oa#')
prov = Namespace('http://www.w3.org/ns/prov#')



def annotate_with_offset(prog_uri,annotations,annotator,relevance,start,end,rdf_graph)
	ann_id = BNode()
	rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
	for annotation in annotations:
		if 'http://' in annotation:
			rdf_graph.add((ann_id,oa['hasBody'],URIRef(annotation)))
		else:
			rdf_graph.add((ann_id,oa['hasBody'],Literal(annotation)))
		
	rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef(annotator)))
	target_id = BNode()
	rdf_graph.add((ann_id,oa['hasTarget'],target_id))
	rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))
	
	for k,v in relevance:
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(value,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef(prov)))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(k)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef(prov)))
	
	selector_id=BNode()
	rdf_graph.add((target_id,oa['hasSelector'],selector_id))
	rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
	rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
	rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
	
	return rdf_graph
	
def annotate_with_offset_and_type(prog_uri,annotations,types,annotator,relevance,start,end,rdf_graph)
	ann_id = BNode()
	rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
	for type in types:
		rdf_graph.add((ann_id,rdf['type'],Literal[type]))
	for annotation in annotations:
		if 'http://' in annotation:
			rdf_graph.add((ann_id,oa['hasBody'],URIRef(annotation)))
		else:
			rdf_graph.add((ann_id,oa['hasBody'],Literal(annotation)))
		
	rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef(annotator)))
	target_id = BNode()
	rdf_graph.add((ann_id,oa['hasTarget'],target_id))
	rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))
	
	for k,v in relevance:
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(value,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef(prov)))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(k)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef(prov)))
	
	selector_id=BNode()
	rdf_graph.add((target_id,oa['hasSelector'],selector_id))
	rdf_graph.add((selector_id,rdf['type'],oa['TextPositionSelector']))
	rdf_graph.add((selector_id,oa['start'],Literal(start,datatype=XSD.integer)))
	rdf_graph.add((selector_id,oa['end'],Literal(end,datatype=XSD.integer)))
	return rdf_graph
	
def annotate_without_offset(prog_uri,annotations,annotator,relevance,rdf_graph)
	ann_id = BNode()
	rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
	for annotation in annotations:
		if 'http://' in annotation:
			rdf_graph.add((ann_id,oa['hasBody'],URIRef(annotation)))
		else:
			rdf_graph.add((ann_id,oa['hasBody'],Literal(annotation)))
		
	rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef(annotator)))
	target_id = BNode()
	rdf_graph.add((ann_id,oa['hasTarget'],target_id))
	rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))
	for k,v in relevance:
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(value,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef(prov)))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(k)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef(prov)))
	return rdf_graph
	
def annotate_without_offset_and_type(prog_uri,annotations,types,annotator,relevance,start,end,rdf_graph)
	ann_id = BNode()
	rdf_graph.add((ann_id,rdf['type'],oa['Annotation']))
	for type in types:
		rdf_graph.add((ann_id,rdf['type'],Literal[type]))
	for annotation in annotations:
		if 'http://' in annotation:
			rdf_graph.add((ann_id,oa['hasBody'],URIRef(annotation)))
		else:
			rdf_graph.add((ann_id,oa['hasBody'],Literal(annotation)))
		
	rdf_graph.add((ann_id,prov['wasGeneratedBy'],URIRef(annotator)))
	target_id = BNode()
	rdf_graph.add((ann_id,oa['hasTarget'],target_id))
	rdf_graph.add((target_id,oa['hasSource'],URIRef(prog_uri)))
	
	for k,v in relevance:
		ann_id2 = BNode()
		rdf_graph.add((ann_id2,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id2,oa['hasBody'],Literal(value,datatype=XSD.float)))
		rdf_graph.add((ann_id2,oa['hasTarget'],ann_id))
		rdf_graph.add((ann_id2,prov['wasGeneratedBy'],URIRef(prov)))
		ann_id4 = BNode()
		rdf_graph.add((ann_id4,rdf['type'],oa['Annotation']))
		rdf_graph.add((ann_id4,oa['hasBody'],Literal(k)))
		rdf_graph.add((ann_id4,oa['hasTarget'],ann_id2))
		rdf_graph.add((ann_id4,prov['wasGeneratedBy'],URIRef(prov)))
	return rdf_graph