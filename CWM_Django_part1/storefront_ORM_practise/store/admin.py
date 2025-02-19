from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    
    
    # computed fields
    @admin.display(ordering='inventory')
    def inventory_status(self, obj):
        if obj.inventory < 10:
            return 'Low'
        return 'OK'
    
    
    def collection_title(self, obj):
        return obj.collection.title


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    
    

# Register your models here.
admin.site.register(models.Product, ProductAdmin)

admin.site.register(models.Customer, CustomerAdmin)