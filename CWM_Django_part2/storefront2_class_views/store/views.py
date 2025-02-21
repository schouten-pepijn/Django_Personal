from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Class-based views
class ProductList(APIView):
    # define get request
    def get(self, request):
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        # Validate the post request
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ProductDetail(APIView):
    
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
def product_list_legacy(request):
    return HttpResponse('List of products')


def product_detail_legacy(request, id):
    return HttpResponse(id)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = (Collection
                    .objects
                    .annotate(product_count=Count('products'))
                    .all()
        )
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            product_count=Count('products')
        ),
        pk=pk
    )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
