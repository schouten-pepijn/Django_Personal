from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
def product_list_legacy(request):
    return HttpResponse('List of products')


def product_detail_legacy(request, id):
    return HttpResponse(id)


# add posting (adding)
@api_view(['GET', 'POST'])
def product_list(request):
    # Serializing
    if request.method == 'GET':
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
    # Deserializing
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # Validate the post request
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# add put (update)
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    # Serializing
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    # Deserializing
    elif request.method == 'PUT':
        serializer = ProductSerializer(
            product,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request, pk):
    return Response('ok')
