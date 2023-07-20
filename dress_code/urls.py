
from django.urls import path
from .views import (HomepageView, LoginView, RegisterView, ContactFromLoginView,
                    logout_user, DataCollectionView, AboutView, AnalysisView)


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth-contact/', ContactFromLoginView.as_view(), name='auth-contact'),
    path('about/', AboutView.as_view(), name='about'),

    path('data-collection/', DataCollectionView.as_view(), name='data-collection'),
    path('analyze-image/', AnalysisView.as_view(), name='analyze-image'),
    path('logout/', logout_user, name='logout'),
]
