from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .utils import fetch_nodes, fetch_node_details
from collection.models import Collection, Publication, PubRating
from collection.views import create_pub


# Create your views here.
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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search/node_details.html'

    def get(self, request):
        node_info = {
            'node_type': request.GET.get('t', ''),
            'node_id': int(request.GET.get('id')),
        }
        node_details = fetch_node_details(node_info)

        if Publication.objects.filter(paperID=node_details["node_properties"]["pubID"]).exists() == False:
            create_pub(node_details["node_properties"]["pubID"])

        pub = Publication.objects.get(paperID=node_details["node_properties"]["pubID"])

        if PubRating.objects.filter(publication=pub, user=request.user).exists():
            pubRating = PubRating.objects.get(publication=pub, user=request.user)
            rating = pubRating.rating

        else:
            rating = 0

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