import re
from .nodeutils import NodeUtils
from neomodel import (
	StringProperty,
	ArrayProperty,
	StructuredNode,
	RelationshipTo,
	RelationshipFrom,
	Relationship
)

class Publication(StructuredNode, NodeUtils):
	venueName = StringProperty()
	references = ArrayProperty()
	year = StringProperty()
	venueID = StringProperty()
	fosWeights = ArrayProperty()
	authorNames = ArrayProperty()
	pubID = StringProperty(index=True)
	publisher = StringProperty()
	title = StringProperty()
	authorIDs = ArrayProperty()
	fosNames = ArrayProperty()
	doi = StringProperty()
	author = RelationshipTo('.author.Author', 'AUTHORED_BY')
	fos = RelationshipTo('.fos.FoS', 'IN_FIELD')
	publicationRel = RelationshipTo('.publication.Publication', 'REFERENCES')
	publisherRel = RelationshipTo('.publisher.Publisher', 'PUBLISHED_BY')
	venue = RelationshipTo('.venue.Venue', 'PUBLISHED_AT')
	

	@property
	def serialize(self):
		return {
			'node_properties': {
				'venueName': self.venueName,
				'references': self.references,
				'year': self.year,
				'venueID': self.venueID,
				'fosWeights': self.fosWeights,
				'authorNames': self.authorNames,
				'pubID': self.pubID,
				'publisher': self.publisher,
				'title': self.title,
				'authorIDs': self.authorIDs,
				'fosNames': self.fosNames,
				'doi': self.doi,
			},
		}

	@property
	def serialize_connections(self):
		return [
			{
				'nodes_type': 'Publication',
				'nodes_related': self.serialize_relationships(self.publication.all()),
			},
			{
				'nodes_type': 'Author',
				'nodes_related': self.serialize_relationships(self.author.all()),
			},
			{
				'nodes_type': 'Venue',
				'nodes_related': self.serialize_relationships(self.venue.all()),
			},
			{
				'nodes_type': 'Publisher',
				'nodes_related': self.serialize_relationships(self.publisher.all()),
			},
			{
				'nodes_type': 'FoS',
				'nodes_related': self.serialize_relationships(self.fos.all())
			},
		]

