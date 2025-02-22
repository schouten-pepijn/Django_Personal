from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem, Product, Collection, Review

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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date',
                  'name', 'description',
        ]
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, obj: CartItem) -> float:
        return obj.product.unit_price * obj.quantity


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


    def save(self, **kwargs):
        cart_id = self.context['cart_pk']
        product_id =self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance


    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No such product')
        return value



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, obj: Cart) -> float:
        return sum(item.quantity * item.product.unit_price for item in obj.items.all())

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
