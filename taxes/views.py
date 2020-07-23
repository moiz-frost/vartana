from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# function based view
def some_view(request):
    emp = {
        'id': 123
    }
    return JsonResponse(emp)
