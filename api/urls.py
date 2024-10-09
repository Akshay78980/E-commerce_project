from django.urls import path
from products.views import CreateProductsAPI,GetProductsAPI,UpdateProductAPI,DeleteProductAPI,\
      CategoryListAPI, CategoryCreateAPI, CategoryUpdateAPI, CategoryDeleteAPI

urlpatterns = [
    path("product/create/",CreateProductsAPI.as_view(),name='product_create'),
    path("product/<int:id>/",GetProductsAPI.as_view(),name='view_product'),
    path("product/",GetProductsAPI.as_view(),name='list_products'),
    path("product/<int:id>/update/",UpdateProductAPI.as_view(),name='update_product'),
    path("product/<int:id>/delete/",DeleteProductAPI.as_view(),name='delete_product'),

    path("category/<int:id>/",CategoryListAPI.as_view(),name='view_category'),
    path("category/",CategoryListAPI.as_view(),name='list_category'),
    path("category/create/",CategoryCreateAPI.as_view(),name='create_category'),
    path("category/<int:id>/update/",CategoryUpdateAPI.as_view(),name='update_category'),
    path("category/<int:id>/delete/",CategoryDeleteAPI.as_view(),name='create_category'),

]