"""
Views based on Paradise Paper Search App’s Django + Neomodel Tutorial
See: https://neo4j-examples.github.io/paradise-papers-django/
"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .utils import fetch_nodes, fetch_node_details
from collection.models import Collection, Publication, PubRating
from collection.views import create_pub


# Define the views for the Search app

from .utils import (
    count_nodes,
    fetch_nodes,
    fetch_node_details
)

class GetNodesCount(APIView):
    def get(self, request):
        count_info = {
            'node_type': request.GET.get('t', ''),
            'search': request.GET.get('q', ''),
            'pub_property': request.GET.get('pp', ''),
        }
        count = count_nodes(count_info)
        data = {
            'response': {
                'status': '200',
                'data': count,
            },
        }
        return Response(data)

class GetNodesData(APIView):
    # View for search results
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search/search_results.html'

    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('t', ''),
            'search': request.GET.get('q', ''),
            'pub_property': request.GET.get('pp', ''),
            'limit': 100,
            'page': int(request.GET.get('p', 1)),
        }
        nodes = fetch_nodes(fetch_info)

        user = request.user.id
        node_list = []

        # If results
        if nodes:
            try:
                # If publication nodes, sort by n_citation
                for node in nodes:
                    # N_citation and year conversion (w/o this some appear as floats in results)
                    node["node_properties"]["n_citation"] = int(float(node["node_properties"]["n_citation"]))
                    node["node_properties"]["year"] = int(float(node["node_properties"]["year"]))
                    node_list.append(node["node_properties"])

                    node_list = sorted(node_list, key = lambda i: int(i["n_citation"]), reverse=True)

                    data = {
                        'response': {
                            'status': '200',
                            'user': user,
                            'rows': len(nodes),
                            'data': node_list,
                            'search': fetch_info['search'],
                            'node_type': fetch_info['node_type'],
                            'pub_property': fetch_info['pub_property']
                        },
                    }
            # Else, just return
            except KeyError:
                data = {
                        'response': {
                            'status': '200',
                            'user': user,
                            'rows': len(nodes),
                            'data': nodes,
                            'search': fetch_info['search'],
                            'node_type': fetch_info['node_type'],
                            'pub_property': fetch_info['pub_property']
                        },
                    }
        # If no results           
        else:
            data = {
                        'response': {
                            'status': '200',
                            'user': user,
                            'rows': len(nodes),
                            'data': nodes,
                            'search': fetch_info['search'],
                            'node_type': fetch_info['node_type'],
                            'pub_property': fetch_info['pub_property']
                        },
                    }

        return Response({'results': data['response']})

class GetNodeData(APIView):
    # View for node detail
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search/node_details.html'

    def get(self, request):
        node_info = {
            'node_type': request.GET.get('t', ''),
            'node_id': int(request.GET.get('id')),
        }
        node_details = fetch_node_details(node_info)

        # If Publication is not in SQLite database, add it
        if Publication.objects.filter(paperID=node_details["node_properties"]["pubID"]).exists() == False:
            create_pub(node_details["node_properties"]["pubID"])

        #Get the publication
        pub = Publication.objects.get(paperID=node_details["node_properties"]["pubID"])

        # Get rating if it exists, else set to 0
        if PubRating.objects.filter(publication=pub, user=request.user).exists():
            pubRating = PubRating.objects.get(publication=pub, user=request.user)
            rating = pubRating.rating

        else:
            rating = 0

        # N_citation and year conversion (w/o this some appear as floats in results)
        try:
            node_details["node_properties"]["n_citation"] = int(float(node_details["node_properties"]["n_citation"]))
            node_details["node_properties"]["year"] = int(float(node_details["node_properties"]["year"]))

        except KeyError:
            pass

        data = {
            'response': {
                'status': '200',
                'data': node_details,
                'node_type': node_info['node_type'],
                'rating': rating
            },
        }
        return Response({'details': data['response']})

class GetFoSNodesData(APIView):
    # View for venue recommender search
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'rec/search_results.html'

    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('t', ''),
            'search': request.GET.get('q', ''),
            'pub_property': request.GET.get('pp', ''),
            'limit': 100,
            'page': int(request.GET.get('p', 1)),
        }
        nodes = fetch_nodes(fetch_info)
        user = request.user.id
        data = {
            'response': {
                'status': '200',
                'user': user,
                'rows': len(nodes),
                'data': nodes,
                'search': fetch_info['search'],
                'node_type': fetch_info['node_type'],
                'pub_property': fetch_info['pub_property']
            },
        }

        return Response({'results': data['response']})