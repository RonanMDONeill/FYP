from django import forms

class CreateNewColl(forms.Form):
	name = forms.CharField(label='Name', max_length=200)

#class CreateNewPub(node_details):
	#paperID = node_details["paperID"]
	#title = node_details["title"]
	#authors = node_details["authors"]
	#year = node_details["year"]
	#fos = node_details["fos"]
	#references = node_details["refs"]
	#doi = node_details["doi"]
	#venueName = node_details["venue"]
	#publisher = node_details["publisher"]
