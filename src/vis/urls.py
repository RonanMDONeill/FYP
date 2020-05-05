from django.urls import include, path
from .views import vis_view

urlpatterns = [
    path('<int:userID>/<int:collID>/', vis_view, name='collection_vis')
]