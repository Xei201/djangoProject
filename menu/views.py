from django.shortcuts import render

from menu.models import MenuItem


def menu_page(request):

    return render(request, "menu.html")
