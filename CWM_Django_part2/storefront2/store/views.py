from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    return Response(id)
