from django.urls import include, path
from .views import (
	scholar_view
)

urlpatterns = [
    path('<str:nodeType>/<str:nodeLabel>', scholar_view, name='external')
]