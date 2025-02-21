from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from . import views

from pprint import pprint

# Routers
# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
pprint(router.urls)

# nested router
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
pprint(products_router.urls)

# URLConf
urlpatterns = [
    path('products/legacy', views.product_list_legacy),
    path('products/legacy/<int:id>', views.product_detail_legacy),
    
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:id>', views.ProductDetail.as_view()),
    
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
]