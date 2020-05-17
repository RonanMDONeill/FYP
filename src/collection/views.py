from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from .models import Collection, Publication, ItemList, Author, PubRating
from .forms import CreateNewColl
from search.utils import fetch_node_details

# Define the views for the Collection app

def colllist_view(response, userID):
	# Return all the collections for a user
	user = User.objects.get(id=userID)
	colls = Collection.objects.filter(user=user)
	return render(response, "collection/coll.html", {"colls": colls})

def addtocoll_view(response, userID, nodeID):
	# Return all collections to a user
	user = User.objects.get(id=userID)
	colls = Collection.objects.filter(user=user)

	# If the Publication is not in the SQLite database, add it
	if Publication.objects.filter(paperID=nodeID).exists() == False:
		create_pub(nodeID)

	return render(response, "collection/add_to_coll.html", {"colls": colls, "nodeID": nodeID})

def addedtocoll_view(response, userID, collID, nodeID):
	# Link user, collection, and publication
	user = User.objects.get(id=userID)
	coll = Collection.objects.get(id=collID)
	pub = Publication.objects.get(paperID=nodeID)

	# Check if Publication is already in the collection, if not add it
	if ItemList.objects.filter(collection=coll, publication=pub).exists() == False:
		addedItem = ItemList(collection=coll, publication=pub)
		addedItem.save()

		print("Created new ItemList")
	
	# Return ItemList and collection
	items = ItemList.objects.filter(collection=coll)
	return render(response, "collection/coll_index.html", {"coll": coll, "items": items})

def removefromcoll_view(response, userID, collID, nodeID):
	# Allow a user to remove a publication from a collection
	user = User.objects.get(id=userID)
	coll = Collection.objects.get(id=collID)
	pub = Publication.objects.get(paperID=nodeID)

	return render(response, "collection/remove.html", {"user": user, "coll": coll, "pub": pub})

def removedfromcoll_view(response, userID, collID, nodeID):
	# Remove the selected publication from collection
	coll = Collection.objects.get(id=collID)
	pub = Publication.objects.get(paperID=nodeID)

	# Delete connection
	addedItem = ItemList.objects.get(collection=coll, publication=pub)
	addedItem.delete()

	print("Removed ItemList")
	redirectURL = '/collection/'+str(userID)+'/'+str(collID)+'/'
	return redirect(redirectURL)


def collcreate_view(response):
	# Return Collection creation form
	if response.method == "POST":
		form = CreateNewColl(response.POST)
		if form.is_valid():
			name = form.cleaned_data["name"]
			user = None
			if response.user.is_authenticated:
				user = response.user
			coll = Collection(name=name, user=user)
			coll.save()

		urlString = "/collection/"+str(user.id)+"/"+str(coll.id)	
		return HttpResponseRedirect(urlString)

	else:
		form = CreateNewColl()

	return render(response, "collection/coll_create.html", {"form": form})

def coll_view(response, userID, id):
	# Return user's collections
	coll = Collection.objects.get(id=id)
	items = ItemList.objects.filter(collection=coll)
	user = userID
	return render(response, "collection/coll_index.html", {"user": user, "coll": coll, "items": items})

def deletecoll_view(response, userID, collID):
	# Allow a user to delete a collection
	user = User.objects.get(id=userID)
	coll = Collection.objects.get(id=collID)

	return render(response, "collection/delete.html", {"user": user, "coll": coll})

def deletedcoll_view(response, userID, collID):
	# Delete selected collection
	coll = Collection.objects.get(id=collID)

	ItemList.objects.filter(collection=coll).delete()
	print("Deleted ItemLists")

	coll.delete()
	print("Deleted Collection")
	redirectURL = '/collection/'+str(userID)+'/'

	return redirect(redirectURL)

def ratepub_view(request, userID, nodeID, rating):
	# Update rating for a publication
	pub = Publication.objects.get(paperID=nodeID)
	if request.method == "POST" and request.is_ajax():
		if PubRating.objects.filter(publication=pub, user=request.user).exists() == False:
			pubRating = PubRating(publication=pub, user=request.user, rating=rating)
			pubRating.save()
		else:
			pubRating = PubRating.objects.get(publication=pub, user=request.user)
			print(pubRating)
			pubRating.rating = rating
			pubRating.save()
			print("Exists")

		return JsonResponse({"status": "Updated"})

	else:
		return JsonResponse({"status": "Failed"})

def create_pub(nodeID):
	# Retrieve selected node details from Neo4j and add to SQLite database
	node_info = {
		'node_type': "Publication",
		'node_id': nodeID,
	}

	node_details = fetch_node_details(node_info)

	paperID = node_details["node_properties"]["pubID"]
	print("Creating new publication: ", paperID)

	title = node_details["node_properties"]["title"]
	n_citation = int(float(node_details["node_properties"]["n_citation"]))


	authorNames = ""
	if node_details["node_properties"]["authorNames"] != None:
		for i, authorName in enumerate(node_details["node_properties"]["authorNames"]):
			if i:
				authorNames += ", "
			authorNames += str(authorName)

	authorIDs = ""
	if node_details["node_properties"]["authorIDs"] != None:
		for i, authorID in enumerate(node_details["node_properties"]["authorIDs"]):
			if i:
				authorIDs += ", "
			authorIDs += str(authorID)

	year = int(float(node_details["node_properties"]["year"]))

	fos = ""
	if node_details["node_properties"]["fosNames"] != None:
		for i, name in enumerate(node_details["node_properties"]["fosNames"]):
			if i:
				fos += ", "
			fos += str(name)

	references = ""
	if node_details["node_properties"]["references"] != None:
		for i, ref in enumerate(node_details["node_properties"]["references"]):
			if i:
				references += ", "
			references += str(ref)

	doi = node_details["node_properties"]["doi"]
	venueName = node_details["node_properties"]["venueName"]
	publisher = node_details["node_properties"]["publisher"]

	pub = Publication(paperID=paperID, title=title, authorNames=authorNames, authorIDs= authorIDs,year=year, fos=fos, references=references, doi=doi, venueName=venueName, publisher=publisher, n_citation=n_citation)
	pub.save()

	for authID in node_details["node_properties"]["authorIDs"]:
		print("Author ID: " + str(authID))
		if Author.objects.filter(authorID=authID).exists() == False:
			node_info = {
				'node_type': "Author",
				'node_id': authID,
			}

			node_details = fetch_node_details(node_info)

			authorName = node_details["node_properties"]["authorName"]

			coAuthors = ""
			if node_details["node_properties"]["coAuthors"] != None:
				for i, coAuthor in enumerate(node_details["node_properties"]["coAuthors"]):
					if i:
						coAuthors += ", "
					coAuthors += str(coAuthor)

			auth = Author(authorID=authID, authorName=authorName, coAuthors= coAuthors)
			auth.save()
	return
