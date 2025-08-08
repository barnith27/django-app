from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

# Register your models here.
from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin

class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archive product')
def mark_archived(modeladmin: admin.ModelAdmin, requests: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchive product')
def mark_unarchived(modeladmin: admin.ModelAdmin, requests: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_cvs',
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk','name'
    ordering = '-name', 'pk'
    search_fields = 'name', 'description', 'price'
    fieldsets = [
        (None, {
           'fields': ('name', 'description'),
        }),
        ('Price option', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': "Extra options. Field 'archived' is sort delete",
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

#admin.site.register(Product, ProductAdmin)

class ProductInline(admin.StackedInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order)-> str:
        return obj.user.first_name or obj.user.username