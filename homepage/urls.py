
from django.urls import path, include

from .views import HomeView, SendEmails


urlpatterns = [
    path('', HomeView.as_view(), name='senai'),
    path('data-analysis/', include('data_analysis.urls')),
    path('articles/', include('article.urls')),

    path('emails/', SendEmails.as_view(), name='send-email')
]