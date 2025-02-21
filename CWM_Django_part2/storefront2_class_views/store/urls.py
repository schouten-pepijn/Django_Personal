from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/legacy', views.product_list_legacy),
    path('products/legacy/<int:id>', views.product_detail_legacy),
    
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>', views.ProductDetail.as_view()),
    
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
]