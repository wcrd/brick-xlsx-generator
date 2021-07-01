# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:11:10 2020

@author: WillDavidson
"""
from rdflib.plugins.sparql import prepareQuery


def query_all_triples_in_namespace():
    """
    Returns all triples underneath a namespace.
    These triples should be iterated over and added to a new graph.
    Namespaces need to be manually bound to the new graph as they do not transfer with this query
    
    Parameters to pass to Graph query: 
    initBindings = { 'namespace': NAMESPACE }
    """
    queryBody = \
        """
        CONSTRUCT {
            ?s ?p ?o
        }
        WHERE { 
            ?s ?p ?o
            FILTER (isURI(?s) && STRSTARTS(str(?s), str(?namespace) ) )
        }
        """
        
    return prepareQuery(queryBody)


def generate_inverse_relationships():
    """
    Generate all valid inverse relationships for a given graph
    """
    queryBody = \
        """
        INSERT {
            ?o ?invprop ?s
        } WHERE {
            ?s ?prop ?o .
            ?prop owl:inverseOf ?invprop
        }
        """
    return queryBody


def query_equipment_and_location_triples_in_namespace(namespaces):
    """
    Returns all equipment and location triples underneath a namespace.
    These triples should be iterated over and added to a new graph.
    Namespaces need to be manually bound to the new graph as they do not transfer with this query

    Parameters to pass to Graph query:
    initBindings = { 'namespace': NAMESPACE }
    """
    queryBody = \
        """
        CONSTRUCT {
            ?s ?p ?o
        }
        WHERE { 
          ?s ?p ?o .
          ?s rdf:type/rdfs:subClassOf* ?class .
          VALUES ?class { brick:Equipment brick:Location brick:System }
          FILTER (isURI(?s) && STRSTARTS(str(?s), str(?namespace) ) )
          MINUS {
            ?o rdf:type/rdfs:subClassOf* brick:Point
          }
        }
        """

    return prepareQuery(queryBody, initNs=namespaces)
