from django.urls import include, path
from .views import (
	colllist_view,
	collcreate_view,
	coll_view,
	addtocoll_view,
	addedtocoll_view,
	removefromcoll_view,
	removedfromcoll_view,
	deletecoll_view,
	deletedcoll_view,
	ratepub_view
)

urlpatterns = [
    path('<int:userID>/', colllist_view, name='collection_list'),
    path('create/', collcreate_view, name='collection_create'),
    path('<int:userID>/<int:id>/', coll_view, name='collection'),
    path('<int:userID>/<int:nodeID>/add/', addtocoll_view, name='add'),
    path('<int:userID>/<int:collID>/<int:nodeID>/', addedtocoll_view, name='added'),
    path('<int:userID>/<int:collID>/<int:nodeID>/remove/', removefromcoll_view, name='remove'),
    path('<int:userID>/<int:collID>/<int:nodeID>/removed/', removedfromcoll_view, name='removed'),
    path('<int:userID>/<int:collID>/delete/', deletecoll_view, name='delete'),
    path('<int:userID>/<int:collID>/deleted/', deletedcoll_view, name='deleted'),
    path('rate/<int:userID>/<int:nodeID>/<int:rating>', ratepub_view, name='rate')
]