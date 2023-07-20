
from django.urls import path
from .views import DataAnalysisView


urlpatterns = [
    path('<str:project_name>/', DataAnalysisView.as_view(), name='data-analysis')
]

