from django.shortcuts import render
import scholarly

# Define the views for the External app

def scholar_view(request, nodeType, nodeLabel):
	# Call scholarly library to retrieve Google Scholar information

	mostCited = None

	# If request is for an Author
	if nodeType == "Author":
		try:
			query = scholarly.search_author(nodeLabel)
			result = next(query).fill()
			mostCited = result.publications[0].fill()

		# If Author cannot be found
		except Exception as e:
			result = "Sorry, we could not find this author's profile."
			nodeType = "Bad query"
			mostCited = None

	# If request is for a Publicaiton
	elif nodeType == "Publication":
		try:
			query = scholarly.search_pubs_query(nodeLabel)
			result = next(query)
			print(result)

		# If Publication cannot be found
		except Exception as e:
			result = "Sorry, we could not find this paper's profile."
			nodeType = "Bad query"

	return render(request, "external/google_search_results.html", {"result": result, "nodeType": nodeType, "mostCited": mostCited})
