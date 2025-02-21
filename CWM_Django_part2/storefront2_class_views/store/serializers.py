from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection

# nested serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
        
    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # collection = CollectionSerializer()
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    def get_price_with_tax(self, obj: Product) -> float:
        return obj.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug',
                  'inventory', 'description', 'unit_price',
                  'price_with_tax', 'collection'
        ]


# verbose and repeated implementation
"""
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # custom name
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # custom method field
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    # serializing relationships (first method)
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    # serializing relationships (second method)
    collection_title = serializers.StringRelatedField(source='collection')
    
    # nested serializer
    collection_nested = CollectionSerializer(source='collection')
    
    # Hyperlink serializer
    collection_link = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail',
        lookup_field='pk',
        source='collection'
    )
"""

"""
    def get_price_with_tax(self, obj: Product) -> float:
        return obj.unit_price * Decimal(1.1)
"""