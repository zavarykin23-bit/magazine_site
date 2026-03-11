#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fish_day_admin.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')
admin_user.save()

print("✅ Пароль установлен: admin / admin123")
