from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/legacy', views.product_list_legacy),
    path('products/legacy/<int:id>', views.product_detail_legacy),
    
    path('products/', views.product_list),
    path('products/<int:id>', views.product_detail),
    
    path('collections/', views.collection_list),
    path('collections/<int:pk>', views.collection_detail, name='collection-detail'),
]