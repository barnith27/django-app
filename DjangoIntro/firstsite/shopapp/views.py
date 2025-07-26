from timeit import default_timer
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def shop_index(request: HttpRequest):
    products = [
        ('laptop', 1000),
        ('desktop', 1600),
        ('smartphone', 600),
    ]
    context = {
        "time_running": default_timer(),
        "products": products
    }
    return render(request, 'shopapp/shop-index.html', context=context)
