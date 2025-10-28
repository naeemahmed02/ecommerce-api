from django.urls import path
from ..views import api_views

urlpatterns = [
    path('categories/', api_views.CategoryCreateListAPIView.as_view(), name='categories_list'),
    path('categories/<slug:category_slug>/', api_views.CategoryDetailAPIView.as_view(), name='category_detail'),
]