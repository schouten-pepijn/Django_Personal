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
router.register('cart', views.CartViewSet)
pprint(router.urls)

# nested router
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
pprint(products_router.urls)

carts_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
    
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:id>', views.ProductDetail.as_view()),
    
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
]