from django.shortcuts import render
from django.db.models import Q, F

from store.models import Collection, Product, OrderItem, Order

from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):
    
    # Products: inventory < 10 OR unit_price < 20
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20)
    # ).order_by('-unit_price')[10:30]
    
    # Products: inventory = price
    # queryset = Product.objects.filter(inventory=F('unit_price'))
    
    # queryset = Product.objects.values('id', 'title')
    
    # specify fields
    # querysetOrderItems = OrderItem.objects \
    #     .values('product__id') \
    #         .distinct()
    # queryset = Product.objects \
    #     .filter(id__in=querysetOrderItems) \
    #         .order_by('id')
    
    queryset = Order.objects \
        .select_related('customer') \
            .prefetch_related('orderitem_set__product') \
                .order_by('-placed_at')[:5]
    
    # ContentType.objects.get_for_models(Product, TaggedItem)
    


    return render(request, 'hello.html', {'name': 'Mosh', 'orders': list(queryset)})