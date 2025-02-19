from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
def product_list_legacy(request):
    return HttpResponse('List of products')


def product_detail_legacy(request, id):
    return HttpResponse(id)


@api_view()
def product_list(request):
    return Response('List of products')


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    data = serializer.data
    return Response(data)
