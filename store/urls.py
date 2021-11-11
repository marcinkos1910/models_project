from django.urls import path
from django.views.generic import DetailView

from store import views, models

app_name = 'store'
urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('product/<int:pk>/', DetailView.as_view(model=models.Product), name="product-detail"),
]
