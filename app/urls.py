from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router
router = DefaultRouter()

# Register your viewsets with the router
router.register(r'items', views.ItemViewSet)

# Define your custom API views
urlpatterns = [
    path('', include(router.urls)),  # Include the viewsets from the router
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='item-detail'),  # Detail view for a single item
]
