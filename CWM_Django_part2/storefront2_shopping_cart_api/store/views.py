from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from .pagination import DefaultPagination

from .filters import ProductFilter
from .models import Cart, Product, Collection, OrderItem, Review, CartItem
from .serializers import CartItemSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer


# Combine the logic of the complete API in one set
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    
    # pagination_class = PageNumberPagination

    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ReadOnlyModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer


    def destroy(self ,request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        product_id = self.kwargs['product_pk']
        return {'product_id': product_id}


class CartViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
    
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')