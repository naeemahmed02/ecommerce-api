from django.urls import path
from .. views import api_views

urlpatterns = [
    path('create-account/', api_views.AccountRegisterationAPIView.as_view(), name='create-user'),
    path('login/', api_views.AccountLoginAPIView.as_view(), name='login'),
]