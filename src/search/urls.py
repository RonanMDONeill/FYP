from django.urls import include, path
from pages.views import search_view
from .views import (
    GetNodesCount,
    GetNodesData,
    GetNodeData,
    GetFoSNodesData
)

urlpatterns = [
	path('', search_view, name='search'),
    path('count/', GetNodesCount.as_view(), name='get_nodes_count'),
    path('nodes/', GetNodesData.as_view(), name='get_nodes_data'),
    path('node/', GetNodeData.as_view(), name='get_node_data'),
    path('venuerec/nodes/', GetFoSNodesData.as_view(), name='get_fos_data')
]