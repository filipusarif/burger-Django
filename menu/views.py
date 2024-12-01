from django.shortcuts import render, get_object_or_404
from .models import Burger
from main.decorators import role_required

def menu_list(request):
    burgers = Burger.objects.all()
    return render(request, 'menu_list.html', {'burgers': burgers})
