from django.urls import include, path
from .views import (
    GetNodesCount,
    GetNodesData,
    GetNodeData,
    GetFoSNodesData
)

# Define the URL paths for the Collection app
urlpatterns = [
    path('count/', GetNodesCount.as_view(), name='get_nodes_count'),
    path('nodes/', GetNodesData.as_view(), name='get_nodes_data'),
    path('node/', GetNodeData.as_view(), name='get_node_data'),
    path('venuerec/nodes/', GetFoSNodesData.as_view(), name='get_fos_data')
]