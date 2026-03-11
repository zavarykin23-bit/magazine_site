# -*- coding: utf-8 -*-
"""
URL маршруты для приложения requests_app
"""
from django.urls import path
from django.http import JsonResponse
from . import views

app_name = 'requests_app'

# Главная страница API
def api_list(request):
    """Список доступных API endpoints"""
    return JsonResponse({
        'status': 'ok',
        'message': 'API endpoints',
        'endpoints': {
            'submit_request': '/api/submit-request/ (POST)',
            'request_list': '/api/requests/ (GET)',
        }
    })

urlpatterns = [
    # Главная страница API
    path('', api_list, name='api_list'),
    
    # API для приема заявок
    path('submit-request/', views.submit_request, name='submit_request'),
    
    # API для получения списка заявок (для админа)
    path('requests/', views.request_list, name='request_list'),
]
