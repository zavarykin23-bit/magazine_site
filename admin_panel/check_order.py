#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fish_day_admin.settings')

# Инициализируем Django
django.setup()

# Теперь можем использовать модели
from requests_app.models import CustomerRequest

# Получаем последний заказ
latest_order = CustomerRequest.objects.latest('created_at')
print(f"✅ Latest order: {latest_order}")
print(f"   ID: {latest_order.id}")
print(f"   Name: {latest_order.name}")
print(f"   Phone: {latest_order.phone}")
print(f"   Order Total: {latest_order.order_total}₽")
print(f"   Order Details length: {len(latest_order.order_details) if latest_order.order_details else 0} bytes")
print(f"   Order Details (first 200 chars): {latest_order.order_details[:200] if latest_order.order_details else 'EMPTY'}")
print()
print("Items list:")
items = latest_order.get_order_items_list()
for i, item in enumerate(items, 1):
    print(f"  {i}. {item.get('name', 'Unknown')} - {item.get('price')}₽ x {item.get('quantity', item.get('customWeight', '?'))}")
