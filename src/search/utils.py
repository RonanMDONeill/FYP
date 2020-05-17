"""
Utils based on Paradise Paper Search App’s Django + Neomodel Tutorial
See: https://neo4j-examples.github.io/paradise-papers-django/
"""

from neomodel import db
from .models import (
	Publication,
	Author,
	Venue,
	Publisher,
	FoS
)


MODEL_ENTITIES = {
	'Publication': Publication,
	'Author': Author,
	'Venue': Venue,
	'Publisher': Publisher,
	'FoS': FoS
}


def filter_nodes(node_type, search_text, publication_property):
	# Filters nodes from Neo4j based on search query
	node_set = node_type.nodes

	# Publication node type
	if node_type.__name__ == "Publication":
		if publication_property == "paperID":
			node_set.filter(pubID=search_text)
		elif publication_property == "title":
			node_set.filter(title__icontains=search_text)
		elif publication_property == "authorNames":
			results, meta = db.cypher_query("MATCH (p:Publication) WHERE {search_text} IN p.authorNames RETURN p LIMIT 100", {'search_text': search_text})
			node_set = [Publication.inflate(row[0]) for row in results]
		elif publication_property == "authorIDs":
			results, meta = db.cypher_query("MATCH (p:Publication) WHERE {search_text} IN p.authorIDs RETURN p LIMIT 100", {'search_text': search_text})
			node_set = [Publication.inflate(row[0]) for row in results]
		elif publication_property == "publisher":
			node_set.filter(publisher__icontains=search_text)
		elif publication_property == "year":
			node_set.filter(year__icontains=search_text)
		elif publication_property == "venueName":
			node_set.filter(venueName__icontains=search_text)
		elif publication_property == "fosNames":
			results, meta = db.cypher_query("MATCH (p:Publication) WHERE {search_text} IN p.fosNames RETURN p LIMIT 100", {'search_text': search_text})
			node_set = [Publication.inflate(row[0]) for row in results]

	# Author node type
	elif node_type.__name__ == "Author":
		if publication_property == "authorID":
			node_set.filter(authorID=search_text)
		else:
			node_set.filter(authorName__icontains=search_text)

	# Venue node type
	elif node_type.__name__ == "Venue":
		node_set.filter(venueName__icontains=search_text)

	# Publisher node type
	elif node_type.__name__ == "Publisher":
		node_set.filter(publisher__icontains=search_text)

	# FoS node type
	elif node_type.__name__ == "FoS":
		node_set.filter(fosName__icontains=search_text)

	return node_set

# Count the filtered nodes
def count_nodes(count_info):
	count = {}
	node_type = count_info["node_type"]
	search_text = count_info["search"]
	pub_property = count_info["pub_property"]
	node_set = filter_nodes(MODEL_ENTITIES[node_type], search_text, pub_property)
	count['count'] = len(node_set)

	return count

# Fetch the nodes based on the search type
def fetch_nodes(fetch_info):
	node_type = fetch_info["node_type"]
	search_text = fetch_info["search"]
	limit = fetch_info["limit"]
	pub_property = fetch_info["pub_property"]
	start = ((fetch_info["page"] - 1) * limit)
	end = start + limit
	node_set = filter_nodes(MODEL_ENTITIES[node_type], search_text, pub_property)
	fetched_nodes = node_set[start:end]

	return [node.serialize for node in fetched_nodes]

# Fetch the details of the specified nodes
def fetch_node_details(node_info):
	node_type = node_info["node_type"]
	node_id = node_info["node_id"]
	if node_type == "Publication":
		node = MODEL_ENTITIES[node_type].nodes.get(pubID=node_id)
	else:
		node = MODEL_ENTITIES[node_type].nodes.get(authorID=node_id)
	node_details = node.serialize

	node_details["node_connections"] = []
	if (hasattr(node, "serialize_connections")):
		node_details["node_connections"] = node.serialize_connections
		
	return node_details