from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.models import Group
from timeit import default_timer


def shop_index(request: HttpRequest):
    context = {
        "time_running": default_timer(),
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)
