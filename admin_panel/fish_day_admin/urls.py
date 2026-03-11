"""
URL configuration for fish_day_admin project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
import os

# Главная страница API
@require_http_methods(["GET"])
def api_home(request):
    """Главная страница API"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Рыбный день - API сервер',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'submit_request': '/api/submit-request/',
        }
    })

# Favicon для браузера (чтобы не было 404)
@require_http_methods(["GET"])
def favicon(request):
    """Favicon для браузера"""
    return HttpResponse(status=204)  # No content

# Обслуживание фронтенд файлов
@require_http_methods(["GET"])
def serve_frontend_file(request, filename='', filename_prefix=''):
    """Обслуживает фронтенд файлы из папки 'рыбный день'"""
    frontend_dir = settings.FRONTEND_DIR
    
    # Если есть префикс (для маршрута assets), добавляем его
    if filename_prefix:
        filename = os.path.join(filename_prefix, filename)
    
    # Если файл не указан или это главная страница - показываем index.html
    if not filename or filename == '':
        filepath = os.path.join(frontend_dir, 'index.html')
    else:
        filepath = os.path.join(frontend_dir, filename)
    
    # Безопасность - не позволяем выходить за пределы папки
    if not os.path.abspath(filepath).startswith(os.path.abspath(frontend_dir)):
        return HttpResponse('Not Found', status=404)
    
    # Если файл существует - обслуживаем его
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Определяем тип контента по расширению
            content_type = 'text/html'
            if filename.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif filename.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif filename.endswith('.png'):
                content_type = 'image/png'
            elif filename.endswith('.gif'):
                content_type = 'image/gif'
            elif filename.endswith('.svg'):
                content_type = 'image/svg+xml'
            
            return HttpResponse(content, content_type=content_type)
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    
    return HttpResponse('Not Found', status=404)

urlpatterns = [
    # Фронтенд маршруты
    path('', serve_frontend_file, name='home'),  # Главная страница
    path('index.html', serve_frontend_file, {'filename': 'index.html'}, name='index'),
    path('product.html', serve_frontend_file, {'filename': 'product.html'}, name='product'),
    path('cart.html', serve_frontend_file, {'filename': 'cart.html'}, name='cart'),
    path('assets/<path:filename>', serve_frontend_file, {'filename_prefix': 'assets'}, name='assets'),
    
    # API маршруты
    path('api/home/', api_home, name='api_home'),
    path('favicon.ico', favicon, name='favicon'),
    path('admin/', admin.site.urls),
    path('api/', include('requests_app.urls')),
]

# Обслуживание медиа файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
