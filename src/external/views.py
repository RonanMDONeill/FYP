from django.shortcuts import render
import scholarly

# Create your views here.
def scholar_view(request, nodeType, nodeLabel):
	if nodeType == "Author":
		try:
			query = scholarly.search_author(nodeLabel)
			result = next(query).fill()
			mostCited = result.publications[0].fill()

		except Exception as e:
			result = "Sorry, we could not find this author's profile."
			nodeType = "Bad query"
			mostCited = None

	elif nodeType == "Publication":
		try:
			query = scholarly.search_pubs_query(nodeLabel)
			result = next(query)
			mostCited = None
			print(result)
		except Exception as e:
			result = "Sorry, we could not find this paper's profile."
			nodeType = "Bad query"
			mostCited = None

	return render(request, "external/google_search_results.html", {"result": result, "nodeType": nodeType, "mostCited": mostCited})
