from django.urls import path
from . import views

urlpatterns = [
    # Static URLs
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),

    # Dynamic URLs
    path(
        'products/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),

    path('categories/', views.category_list, name='category_list'),

    # Example with slug
    path(
        'categories/<str:slug>/',
        views.category_detail,
        name='category_detail'
    ),

    path(
        'products/add',
        views.product_create,
        name ='product_create'
    ),

    path(
        'products/<int:pk>/edit/',
        views.product_update,
        name='product_update'
    ),

    path(
        'products/<int:pk>/delete/',
        views.product_delete,
        name='product_delete'
    ),


# REST API Endpoints
path('api/products/', views.ProductListCreateAPIView.as_view(), name='product_list_api'),

path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product_detail_api'),

path('api/categories/', views.CategoryListAPIView.as_view(), name='category_list_api'),
]

