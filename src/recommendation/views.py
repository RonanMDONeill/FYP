from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework.response import Response

from .models import RecPub
from collection.models import Collection, Publication, ItemList, PubRating
from search.utils import fetch_node_details, fetch_nodes

import os, nltk, smart_open
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download("punkt")
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.similarities import Similarity
from neomodel.exceptions import DoesNotExist
from collections import Counter

def initiate_recommender():
	baseDir = settings.BASE_DIR

	dictFile = baseDir + "\static\data\DBLP_Dictionary.dict"
	corpusFile = baseDir + "\static\data\DBLP_Corpus.mm"

	dictionary = corpora.Dictionary.load(dictFile)
	corpus = corpora.MmCorpus(corpusFile)

	# Load the TF-IDF model
	tfidfFile = baseDir + "\static\data\TF-IDF"

	tfidf = models.TfidfModel().load(tfidfFile)

	# Load the Gensim similarity index
	indexFile = r"D:/Users/Rónan/Documents/UCD/Stage 4/FYP/Dataset/Index"
	sims = Similarity.load(indexFile)

	# Point to the text csv file
	textFile = baseDir + "\static\data\Text.csv"

	# Load ID dataframe from recommender
	paperIDs = baseDir + "\static\data\AbsID.csv"
	cols = ["paperID"]
	dfIDs = pd.read_csv(paperIDs, names=cols, header=None)

	return dictionary, corpus, tfidf, sims, textFile, dfIDs

def generate_recommendations(dictionary, corpus, tfidf, sims, queryText, dfIDs, recNum, paperID_list, indices):
	query = [w for w in word_tokenize(queryText)]
	queryBoW = dictionary.doc2bow(query)

	print(queryText)

	#Generate the similarity of the paper to every other paper
	queryTfidf = tfidf[queryBoW]
	querySim = sims[queryTfidf]

	# Join ID dataframe and similarity series
	df = dfIDs

	df["sim"]=pd.Series(querySim)

	# Drop query papers
	df = df.drop(indices, axis=0)

	# Sort by similarity
	df = df.sort_values(by="sim", ascending=False)

	# Get top N results
	df = df["paperID"].head(recNum)

	top5 = df.tolist()

	paperID_list.extend(top5)

	# Clear variables from memory
	index = None
	line = None
	query = None
	queryBoW = None
	queryTfidf = None
	querySim = None
	df = None
	top5 = None

	return paperID_list

def get_pubs(paperID_list):
	pub_list = []
	# Return RecPub, if it doesn't exist, create
	for nodeID in paperID_list:
		try:
			if Publication.objects.filter(paperID=nodeID).exists() == False:
				node_info = {
					'node_type': "Publication",
					'node_id': nodeID,
				}

				node_details = fetch_node_details(node_info)

				paperID = node_details["node_properties"]["pubID"]
				print("Creating new publication: ", paperID)

				title = node_details["node_properties"]["title"]


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

				pub = Publication(paperID=paperID, title=title, authorNames=authorNames, year=year, fos=fos, references=references, doi=doi, venueName=venueName, publisher=publisher)
				pub.save()

			pub_list.append(Publication.objects.get(paperID=nodeID))

		except DoesNotExist:
			pass

	return pub_list

def coll_rec_view(response, userID, collID):
	# Get the paperIDs within the collection
	coll = Collection.objects.get(id=collID)
	items = ItemList.objects.filter(collection=coll)

	dictionary, corpus, tfidf, sims, textFile, dfIDs = initiate_recommender()

	paperID_list = []
	pub_list = []
	index_list = []

	queryText = ""

	for item in items:
		index = dfIDs[dfIDs["paperID"]==item.publication.paperID].index.values[0]
		index_list.append(index)

	index_list.sort()

	with open(textFile, encoding='utf-8') as f:
		for i in range(index_list[-1]):
			line = f.readline()
			if i in index_list:
				queryText += line + " "

	paperID_list = generate_recommendations(dictionary, corpus, tfidf, sims, queryText, dfIDs, 10, paperID_list, index_list)

	# Clear variables from memory
	dictionary = None
	corpus = None
	tfidf = None
	sims = None
	cols = None
	dfIDs = None
	baseDir = None
	dictFile = None
	corpusFile = None
	tfidfFile = None
	indexFile = None
	textFile = None
	paperIDs = None

	pub_list = get_pubs(paperID_list)
	
	return render(response, "rec/coll_rec.html", {"pub_list": pub_list, "coll": coll})

def rec_info_view(response, userID, collID):
	coll = Collection.objects.get(id=collID)
	items = ItemList.objects.filter(collection=coll)

	collText = " "
	collText_dict = {}
	collText_list = []
	collTextUnique_list = []
	index_list = []

	baseDir = settings.BASE_DIR

	paperIDs = baseDir + "\static\data\AbsID.csv"
	cols = ["paperID"]
	dfIDs = pd.read_csv(paperIDs, names=cols, header=None)

	textFile = baseDir + "\static\data\Text.csv"

	for item in items:
		index = dfIDs[dfIDs["paperID"]==item.publication.paperID].index.values[0]
		index_list.append(index)

	index_list.sort()

	with open(textFile, encoding='utf-8') as f:
		for i in range(index_list[-1]):
			line = f.readline()
			if i in index_list:
				collText += line

	for word in collText.split(" "):
		if word not in collText_dict:
			collText_dict[word] = 1
		else:
			if collText_dict[word] == 1:
				collText_list.append(word)

	for word in collText_list:
		if word not in collTextUnique_list and word != "":
			collTextUnique_list.append(word)


	return render(response, "rec/rec_info.html", {"text": collTextUnique_list})

def fos_search_view(response):
	baseDir = settings.BASE_DIR

	fosFile = baseDir + "\static\data\cleanFosName.csv"#

	fosList = []

	with open(fosFile, encoding='utf-8') as f:
		for line in f:
			fosList.append(line)

	print(len(fosList))
	return render(response, "rec/fos_search.html", {"fosNames": fosList})

def rec_venue_view(response, fos):
	fetch_info = {
		'node_type': "Publication",
		'search': fos,
		'pub_property': "fosNames",
		'limit': 500,
		'page': 1,
	}

	nodes = fetch_nodes(fetch_info)

	venueList = []

	for node in nodes:
		properties = node["node_properties"]
		venueList.append(properties["venueName"])

	mostCommonVenue = Counter(venueList).most_common(1)
	venueTuple = mostCommonVenue[0]

	venueName = venueTuple[0]
	print(venueName)

	return render(response, "rec/rec_venue.html", {"venueName": venueName, "fosName": fos})

def rec_rating_view(response, userID):

	ratedPubs = PubRating.objects.filter(user=userID)

	ratedPub_list = []
	for ratedPub in ratedPubs:
		if ratedPub.rating >= 4:
			ratedPub_list.append(ratedPub.publication.paperID)

	if not ratedPub_list:
		pub_list = []

	else:
		dictionary, corpus, tfidf, sims, textFile, dfIDs = initiate_recommender()

		paperID_list = []
		pub_list = []
		index_list = []

		queryText = ""

		for pub in ratedPub_list:
			index = dfIDs[dfIDs["paperID"]==pub].index.values[0]
			index_list.append(index)

		index_list.sort()

		with open(textFile, encoding='utf-8') as f:
			for i in range(index_list[-1]):
				line = f.readline()
				if i in index_list:
					queryText += line + " "

		paperID_list = generate_recommendations(dictionary, corpus, tfidf, sims, queryText, dfIDs, 10, paperID_list, index_list)

		# Clear variables from memory
		dictionary = None
		corpus = None
		tfidf = None
		sims = None
		cols = None
		dfIDs = None
		baseDir = None
		dictFile = None
		corpusFile = None
		tfidfFile = None
		indexFile = None
		textFile = None
		paperIDs = None

		pub_list = get_pubs(paperID_list)

	return render(response, "rec/rating_rec.html", {"pub_list": pub_list})

def rec_rating_info_view(response, userID):
	ratedPubs = PubRating.objects.filter(user=userID)
	pub_list = []

	for pub in ratedPubs:
		if pub.rating >= 4:
			pub_list.append(pub.publication)

	print(pub_list)

	return render(response, "rec/rec_rating_info.html", {"pub_list": pub_list})


