from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

# Register your models here.
from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm

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

    def import_csv(self, request: HttpRequest)->HttpResponse:
        form = CSVImportForm()
        context = {
            'form': form,
        }
        return render(request, 'admin/csv_form.html', context)

    def get_absolute_url(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv',
            )
        ]
        return new_urls + urls

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

#admin.site.register(Product, ProductAdmin)

class ProductInline(admin.StackedInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/orders_changelist.html'
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order)-> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        orders = []
        for row in reader:
            order = Order(
                delivery_address=row['delivery_address'],
                promocode=row['promocode'],
                user_id=row['user_id'],
            )
            orders.append(order)

        Order.objects.bulk_create(orders)

        csv_file.seek(0)
        next(reader)

        for row, order in zip(reader, orders):
            if 'products' in row:
                product_ids = [int(pid) for pid in row['products'].split(',') if pid.strip()]
                products = Product.objects.filter(id__in=product_ids)
                order.products.set(products)

        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='import_orders_csv'
            ),
        ]

        return custom_urls + urls