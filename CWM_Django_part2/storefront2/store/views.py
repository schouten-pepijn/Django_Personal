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


@api_view()
def product_list(request):
    try:
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    data = serializer.data
    return Response(data)


@api_view()
def collection_detail(request, pk):
    return Response('ok')
