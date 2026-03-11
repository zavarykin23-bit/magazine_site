#!/usr/bin/env python
"""
Простой скрипт для проверки что находится в БД
"""
import sqlite3
import json
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"❌ БД не найдена: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем последний заказ
cursor.execute("""
    SELECT id, name, phone, order_details, order_total, created_at 
    FROM requests_app_customerrequest 
    ORDER BY created_at DESC 
    LIMIT 1
""")

row = cursor.fetchone()
conn.close()

if not row:
    print("❌ В БД нет заказов!")
    exit(1)

print("✅ Последний заказ:")
print(f"   ID: {row[0]}")
print(f"   Name: {row[1]}")
print(f"   Phone: {row[2]}")
print(f"   Total: {row[4]}₽")
print(f"   Created: {row[5]}")
print()

order_details = row[3]
if order_details:
    print(f"✅ Order Details ({len(order_details)} bytes):")
    print(f"   Raw: {order_details[:200]}...")
    print()
    
    try:
        items = json.loads(order_details)
        print(f"✅ Parsed JSON - {len(items)} items:")
        for i, item in enumerate(items, 1):
            print(f"   {i}. {item.get('name')} - {item.get('price')}₽")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {str(e)}")
else:
    print("⚠️ Order Details is EMPTY!")
