from django.urls import include, path
from .views import (
	coll_rec_view,
	rec_info_view,
	fos_search_view,
	rec_venue_view,
	rec_rating_view,
	rec_rating_info_view
)

# Define the URL paths for the Recommendation app
urlpatterns = [
    path('<int:userID>/<int:collID>/', coll_rec_view, name='collection recommendations'),
    path('<int:userID>/<int:collID>/info', rec_info_view, name='recommendation information'),
    path('venue', fos_search_view, name='field of study search'),
    path('venue/<str:fos>', rec_venue_view, name='recommended venue'),
    path('<int:userID>', rec_rating_view, name='rating recommendations'),
    path('<int:userID>/info', rec_rating_info_view, name='rating recommendation information')
]