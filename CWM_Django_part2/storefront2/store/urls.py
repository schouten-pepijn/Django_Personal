from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/legacy', views.product_list_legacy),
    
    path('products/<int:id>', views.product_detail),
    path('products/legacy/<int:id>', views.product_detail_legacy),
]