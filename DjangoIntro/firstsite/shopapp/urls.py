from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShopIndexView, GroupsListView, OrdersListView, \
    ProductDetailsView, ProductsListView, OrderDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    OrderCreateView, OrderUpdateView, OrderDeleteView, OrdersExportView, ProductViewSet, OrderViewSet, \
    LatestProductsFeed, UserOrdersListView, UserExportView

app_name = 'shopapp'
router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('',ShopIndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='latest_feed'),

    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/new_order/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/export/', OrdersExportView.as_view(), name='order_export'),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_order_list'),
    path('users/<int:user_id>/orders/export/', UserExportView.as_view(), name='user_export'),
]
