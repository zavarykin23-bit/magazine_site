from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
import json
import logging

from .models import CustomerRequest
from .email_service import send_order_confirmation_email, send_order_notification_to_admin

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Получить IP адрес клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["POST", "OPTIONS"])
@csrf_exempt  # CSRF отключен т.к. форма с фронтенда, нужно добавить токен позже
def submit_request(request):
    """
    API для приема заявок от клиентов
    Endpoint: /api/submit-request/
    """
    
    if request.method == 'OPTIONS':
        # Для CORS preflight requests
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    try:
        # Логирование RAW body
        try:
            raw_body = request.body.decode('utf-8')
            logger.info(f"✅ RAW BODY ({len(raw_body)} bytes): {raw_body[:1000]}")
        except:
            logger.error(f"❌ Could not decode body")
        
        # Получить данные из POST запроса
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Дебаг логирование
        logger.info(f"✅ Request received!")
        logger.info(f"   Content-Type: {request.content_type}")
        logger.info(f"   Data keys: {list(data.keys())}")
        logger.info(f"   Data content: {data}")  # Entire parsed data
        
        # Логируем корзину более подробно
        # Пытаемся получить cart_items (основное имя) или cart (для совместимости)
        cart_data = data.get('cart_items') or data.get('cart')
        if cart_data:
            logger.info(f"   ✅ Cart found! Type: {type(cart_data)}, Length: {len(cart_data) if isinstance(cart_data, (list, dict)) else 'N/A'}")
            if isinstance(cart_data, list) and len(cart_data) > 0:
                logger.info(f"   First item: {cart_data[0]}")
            elif isinstance(cart_data, str):
                logger.info(f"   Cart is string: {cart_data[:200]}")
        else:
            logger.warning(f"   ⚠️ No cart data in request!")
        
        # ===== ЗАЩИТА ОТ СПАМА =====
        
        # 1. Проверка honeypot поля (если оно заполнено - спам)
        honeypot = data.get('honeypot', '')
        if honeypot:
            logger.warning(f"Honeypot triggered from IP {get_client_ip(request)}")
            # Отвечаем как будто все ОК, но в БД не сохраняем
            return JsonResponse({
                'status': 'success',
                'message': 'Спасибо! Ваша заявка принята.'
            })
        
        # 2. Проверка обязательных полей
        required_fields = ['name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Поле "{field}" обязательно'
                }, status=400)
        
        # 3. Базовая валидация телефона (только цифры и знаки +, -, (), пробелы)
        phone = data.get('phone', '').strip()
        if not any(c.isdigit() for c in phone):
            return JsonResponse({
                'status': 'error',
                'message': 'Некорректный номер телефона'
            }, status=400)
        
        # 4. Проверка на дублиминты (одинаковая заявка в течение 5 минут)
        from django.utils.timezone import timedelta
        five_min_ago = now() - timedelta(minutes=5)
        
        duplicate_check = CustomerRequest.objects.filter(
            phone=phone,
            name=data.get('name', ''),
            created_at__gte=five_min_ago
        )
        
        if duplicate_check.exists():
            logger.info(f"Duplicate request from {phone}")
            return JsonResponse({
                'status': 'error',
                'message': 'Похожая заявка уже была отправлена. Пожалуйста, подождите немного.'
            }, status=429)  # Too Many Requests
        
        # ===== СОХРАНЕНИЕ ЗАЯВКИ =====
        
        # Преобразуем order_details в JSON строку, если есть корзина
        raw_details = ''
        # Ищем cart_items (основное имя) или cart (для совместимости)
        cart_to_save = data.get('cart_items') or data.get('cart')
        if cart_to_save:
            try:
                import json as _json
                raw_details = _json.dumps(cart_to_save)
                logger.info(f"✅ Cart serialized successfully: {len(raw_details)} bytes")
            except Exception as e:
                logger.error(f"❌ Failed to serialize cart: {str(e)}")
                raw_details = str(cart_to_save)
        else:
            logger.warning(f"⚠️ No cart data received")
        
        # Получаем общую сумму из данных
        order_total = 0.0
        if data.get('total'):
            try:
                # Пытаемся извлечь число из строки (может быть "1234.56₽")
                total_str = str(data.get('total')).replace('₽', '').strip()
                order_total = float(total_str)
            except (ValueError, TypeError):
                order_total = 0.0
        
        request_obj = CustomerRequest.objects.create(
            # Обязательные поля
            name=data.get('name', '').strip(),
            phone=data.get('phone', '').strip(),
            
            # Опциональные поля
            email=data.get('email', '').strip() or None,
            request_type=data.get('request_type', 'order'),
            product_name=data.get('product_name', '').strip() or None,
            product_weight=data.get('product_weight', '').strip() or None,
            quantity=int(data.get('quantity', 1)) if data.get('quantity') else 1,
            address=data.get('address', '').strip() or None,
            comment=data.get('comment', '').strip() or None,
            
            # Служебные данные
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:200],
            honeypot=honeypot,
            order_details=raw_details,
            order_total=order_total,
            
            # Статус по умолчанию
            status='new'
        )
        
        logger.info(f"✅ New request created: ID={request_obj.id}")
        logger.info(f"   Name={request_obj.name}, Phone={request_obj.phone}")
        logger.info(f"   Order Total={order_total}₽")
        logger.info(f"   Order Details length={len(raw_details)} bytes")
        
        # ===== ОТПРАВКА EMAIL-УВЕДОМЛЕНИЙ =====
        
        # Подготовка данных клиента для письма
        customer_data = {
            'name': request_obj.name,
            'phone': request_obj.phone,
            'email': request_obj.email,
            'address': request_obj.address,
            'comment': request_obj.comment
        }
        
        cart_items = 'Заказ обработан'
        try:
            if data.get('order_details'):
                cart_items = data.get('order_details')
        except:
            pass
        
        total_amount = data.get('total', '0')
        
        try:
            if request_obj.email:
                send_order_confirmation_email(customer_data, cart_items, total_amount)
        except Exception as e:
            logger.error(f"Error sending confirmation email: {str(e)}", exc_info=True)
        
        # 2️⃣ Отправляем письмо АДМИНИСТРАТОРУ
        try:
            send_order_notification_to_admin(customer_data, cart_items, total_amount)
        except Exception as e:
            logger.error(f"Error sending admin notification: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.',
            'request_id': request_obj.id
        })
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request")
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный формат данных'
        }, status=400)
    
    except Exception as e:
        logger.error(f"Error in submit_request: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка при обработке заявки. Попробуйте позже.'
        }, status=500)


@require_http_methods(["GET"])
def request_list(request):
    """
    Получить список заявок (для администратора)
    Требуется аутентификация
    """
    if not request.user.is_staff:
        return JsonResponse({
            'status': 'error',
            'message': 'Доступ запрещен'
        }, status=403)
    
    try:
        # Фильтрация
        queryset = CustomerRequest.objects.all()
        
        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        request_type = request.GET.get('type')
        if request_type:
            queryset = queryset.filter(request_type=request_type)
        
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )
        
        # Пагинация
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        offset = (page - 1) * per_page
        
        total = queryset.count()
        requests = queryset[offset:offset + per_page]
        
        data = []
        for req in requests:
            data.append({
                'id': req.id,
                'name': req.name,
                'phone': req.phone,
                'email': req.email,
                'type': req.request_type,
                'product': req.product_name,
                'status': req.status,
                'created_at': req.created_at.isoformat(),
                'message': req.comment
            })
        
        return JsonResponse({
            'status': 'success',
            'total': total,
            'page': page,
            'per_page': per_page,
            'data': data
        })
    
    except Exception as e:
        logger.error(f"Error in request_list: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Ошибка при получении списка'
        }, status=500)
