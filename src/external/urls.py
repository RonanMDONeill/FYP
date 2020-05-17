from django.urls import include, path
from .views import (
	scholar_view
)

# Define the URL paths for the External app
urlpatterns = [
    path('<str:nodeType>/<str:nodeLabel>', scholar_view, name='external')
]