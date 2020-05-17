from django.urls import include, path
from .views import vis_view, vis_info_view

# Define the URL paths for the Vis app
urlpatterns = [
    path('<int:userID>/<int:collID>/', vis_view, name='collection_vis'),
    path('info/', vis_info_view, name='vis info')
]