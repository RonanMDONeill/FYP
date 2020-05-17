from django.shortcuts import render
from collection.models import Collection, Publication, ItemList, Author
from search.utils import fetch_nodes
from django.core.files.storage import default_storage
from django.conf import settings
import json, re

# Define the views for the vis app

def vis_view(response, userID, collID):
	# View for collection visualizations
	# This is not pretty, but it works...

	# Get collection and ItemList
	coll = Collection.objects.filter(id=collID)
	items = ItemList.objects.filter(collection__in=coll)

	paper_list = []
	author_list = []
	paperID_list = []
	refDict_list = []

	# Publication and Author node-edge lists
	nodePA_list = ""
	nodePAID_list = ""
	nodePAColour_list = ""
	nodePAShape_list = ""
	toEdgePA_list = ""
	fromEdgePA_list = ""

	# Publication node-edge lists
	nodeP_list = ""
	nodePID_list = ""
	nodePColour_list = ""
	nodePShape_list = ""
	toEdgeP_list = ""
	fromEdgeP_list = ""

	# Co-Author node-edge lists
	nodeA_list = ""
	nodeAID_list = ""
	nodeAColour_list = ""
	nodeAShape_list = ""
	toEdgeA_list = ""
	fromEdgeA_list = ""

	# Citation node-edge lists
	nodeC_list = ""
	nodeCID_list = ""
	nodeCColour_list = ""
	nodeCShape_list = ""
	toEdgeC_list = ""
	fromEdgeC_list = ""

	# Recommended Authors lists
	recAuthor_list = []
	recAuthor_checklist = []
	recAuthorDict_checklist = []

	# Recommend Papers lists
	recPaper_list = []
	recPaper_checklist = []
	recPaperDict_checklist = []

	# Lists using for checking throughout
	paper_checklist = []
	author_checklist = []
	coAuthor_checklist = []
	coAuthorDict_checklist = []
	count = 1
	paperID = 1

	# Create Publication and Author dataset
	for x, item in enumerate(items):
		# Collect paper details
		paperID = item.publication.paperID
		paperID_list.append(str(paperID))
		paper_checklist.append(str(paperID))

		paper = {
			"paperID": paperID,
			"title": item.publication.title,
			"authorNames":	item.publication.authorNames,
			"authorIDs": item.publication.authorIDs,
			"year": item.publication.year,
			"fos": item.publication.fos,
			"references": item.publication.references,
			"venueName": item.publication.venueName,
			"publisher": item.publication.publisher,
		}

		# Add paper to list
		paper_list.append(paper)

		# Get each reference of each paper
		for ref in paper["references"].split(","):
			refDict = {
				"paperID": str(paper["paperID"]),
				"ref": ref.lstrip()
			}

			refDict_list.append(refDict)

		# Create paper node
		node =  paper["title"]
		nodeID = str(paperID)

		# Add to necessarym lists, * is used in JavaScript to tokenize the string
		nodePA_list += node + "*"
		nodePAID_list += nodeID + "*"
		nodePAColour_list += "#00bfff*"
		nodePAShape_list += "box*"

		nodeP_list += node + "*"
		nodePID_list += nodeID + "*"
		nodePColour_list += "#00bfff*"
		nodePShape_list += "box*"

		nodeC_list += node + "*"
		nodeCID_list += nodeID + "*"
		nodeCColour_list += "#00bfff*"
		nodeCShape_list += "box*"

		# Get each author for each paper
		for ID in item.publication.authorIDs.split(","):
			# Collect author details
			cleanID = ID.lstrip()
			count += 1

			# If author has not already been come across
			if cleanID not in author_checklist:
				auth = Author.objects.get(authorID=cleanID)

				author = {
					"authorID": auth.authorID,
					"authorName": auth.authorName,
					"coAuthors": auth.coAuthors
				}

				author_list.append(author)

				# Create author node and link
				node = author["authorName"]
				nodeID = str(cleanID)

				nodePA_list += node + "*"
				nodePAID_list += nodeID + "*"
				nodePAColour_list += "#ffff00*"
				nodePAShape_list += "ellipse*"

				nodeA_list += node + "*"
				nodeAID_list += nodeID + "*"
				nodeAColour_list += "#ffff00*"
				nodeAShape_list += "ellipse*"


				fromEdge = str(paperID)
				fromEdgePA_list += fromEdge + "*"

				toEdge = str(cleanID)
				toEdgePA_list += toEdge + "*"

				author_checklist.append(cleanID)

			else:
				fromEdge = str(paperID)
				fromEdgePA_list += fromEdge + "*"

				toEdge = str(cleanID)
				toEdgePA_list += toEdge + "*"


		count += 1

	# Create Reference connections
	for paperID in paperID_list:
		for refDict in refDict_list:
			if refDict["ref"] == str(paperID):
				cleanID = str(paperID).lstrip()

				referencingPaper = refDict["paperID"]

				fromEdge = str(referencingPaper)
				fromEdgePA_list += fromEdge + "*"

				fromEdgeP_list += fromEdge + "*"

				toEdge = str(cleanID)
				toEdgePA_list += toEdge + "*"

				toEdgeP_list += toEdge + "*"

	# Create Co-Author connections
	for author in author_list:
		for coAuthor in author["coAuthors"].split(","):
			coAuthorID = coAuthor.lstrip()
			# If the Co-Author is in the collection
			if coAuthorID in author_checklist:

				checkDict = {
					"from": str(author["authorID"]),
					"to": coAuthorID
				}

				if checkDict not in coAuthorDict_checklist:
					fromEdge = coAuthorID
					fromEdgeA_list += fromEdge + "*"

					toEdge = str(author["authorID"])
					toEdgeA_list += toEdge + "*"

					coAuthorCheck = {
						"from": fromEdge,
						"to": toEdge
					}

					coAuthorDict_checklist.append(coAuthorCheck)

			else:
				# If haven't come across Co-Author yet
				if coAuthorID not in coAuthor_checklist:
					fetch_info = {
						'node_type': "Author",
						'search': coAuthorID,
						'pub_property': "authorID",
						'limit': 100,
						'page': 1,
					}

					node = fetch_nodes(fetch_info)

					if node == []:
						break

					coAuthorName = str(node).split("authorName': ")[1].split(",")[0]
					coAuthorName = coAuthorName[1:-1]

					nodeA_list += coAuthorName + "*"
					nodeAID_list += coAuthorID + "*"
					nodeAColour_list += "#ff0000*"
					nodeAShape_list += "ellipse*"


					fromEdge = str(author["authorID"])
					fromEdgeA_list += fromEdge + "*"

					toEdge = str(coAuthorID)
					toEdgeA_list += toEdge + "*"
					

					coAuthor_checklist.append(coAuthorID)

					recAuthorDict = {
						'authorName': coAuthorName,
						'authorID': coAuthorID
					}

					recAuthorDict_checklist.append(recAuthorDict)

				else:
					fromEdge = str(author["authorID"])
					fromEdgeA_list += fromEdge + "*"

					toEdge = str(coAuthorID)
					toEdgeA_list += toEdge + "*"

	# Get references outside of collection
	for paper in paper_list:
		for ref in str(paper["references"]).split(","):
			refID = ref.lstrip()
			if refID not in paperID_list:
				fetch_info = {
						'node_type': "Publication",
						'search': refID,
						'pub_property': "paperID",
						'limit': 100,
						'page': 1,
					}

				node = fetch_nodes(fetch_info)

				if node == []:
					break
				
				node = node[0]["node_properties"]

				refPaper = {
					"paperID": refID,
					"title": node["title"],
					"authorNames": node["authorNames"],
					"authorIDs": node["authorIDs"],
					"year": node["year"],
					"fos": node["fosNames"],
					"references": node["references"],
					"venueName": node["venueName"],
					"publisher": node["publisher"]
				}

				paper_list.append(refPaper)

				# Create paper node
				node =  refPaper["title"]
				nodeID = refPaper["paperID"]

				nodeC_list += node + "*"
				nodeCID_list += nodeID + "*"
				nodeCColour_list += "#ffa500*"
				nodeCShape_list += "box*"

				fromEdge = str(paper["paperID"])
				fromEdgeC_list += fromEdge + "*"

				toEdge = str(refID)
				toEdgeC_list += toEdge + "*"

				paperID_list.append(refID)

				recPaperDict = {
						'paperName': node,
						'paperID': refID
					}

				recPaperDict_checklist.append(recPaperDict)

			else:
				fromEdge = str(paper["paperID"])
				fromEdgeC_list += fromEdge + "*"

				toEdge = str(refID)
				toEdgeC_list += toEdge + "*"

	# Get recommended Authors
	for author in toEdgeA_list.split("*"):
		if author not in recAuthor_checklist:
			recAuthor_checklist.append(author)
		else:
			if author not in author_checklist:
				authorID = author
				for authorDict in recAuthorDict_checklist:
					if authorDict["authorID"] == authorID:
						authorName = authorDict["authorName"]
				
				authDict = {
					"authorName": authorName,
					"authorID": authorID,
					"count": 1
				}

				if authDict not in recAuthor_list:
					recAuthor_list.append(authDict)

				else:
					for oldDict in recAuthor_list:
						if oldDict["authorName"] == authDict["authorName"] and oldDict["authorID"] == authDict["authorID"]:
							oldDict["count"] = oldDict["count"] + 1

	recAuthor_list = sorted(recAuthor_list, key = lambda i: i["count"], reverse=True)

	# Get recommend Papers
	for paper in toEdgeC_list.split("*"):
		if paper not in recPaper_checklist:
			recPaper_checklist.append(paper)
		else:
			if paper not in paper_checklist:
				paperID = paper
				for paperDict in recPaperDict_checklist:
					if paperDict["paperID"] == paperID:
						paperName = paperDict["paperName"]
				
				paperDict = {
					"paper": paperName,
					"paperID": paperID,
					"count": 1
				}

				if paperDict not in recPaper_list:
					recPaper_list.append(paperDict)

				else:
					for oldDict in recPaper_list:
						if oldDict["paper"] == authDict["paper"] and oldDict["paperID"] == authDict["paperID"]:
							oldDict["count"] = oldDict["count"] + 1

	recPaper_list = sorted(recPaper_list, key = lambda i: i["count"], reverse=True)

	return render(response, "vis/vis.html", {"nodePA_list": nodePA_list, "nodePAID_list": nodePAID_list, "nodePAColour_list": nodePAColour_list, 
		"nodePAShape_list": nodePAShape_list, "fromEdgePA_list": fromEdgePA_list, "toEdgePA_list": toEdgePA_list, "nodeP_list": nodeP_list, 
		"nodePID_list": nodePID_list, "nodePColour_list": nodePColour_list, "nodePShape_list": nodePShape_list, "fromEdgeP_list": fromEdgeP_list, 
		"toEdgeP_list": toEdgeP_list, "nodeA_list": nodeA_list, "nodeAID_list": nodeAID_list, "nodeAColour_list": nodeAColour_list, 
		"nodeAShape_list": nodeAShape_list, "fromEdgeA_list": fromEdgeA_list, "toEdgeA_list": toEdgeA_list, "nodeC_list": nodeC_list, 
		"nodeCID_list": nodeCID_list, "nodeCColour_list": nodeCColour_list, "nodeCShape_list": nodeCShape_list, "fromEdgeC_list": fromEdgeC_list, 
		"toEdgeC_list": toEdgeC_list, "recAuthor_list": recAuthor_list, "recPaper_list": recPaper_list})

def vis_info_view(response):

	return render(response, "vis/info.html", {})