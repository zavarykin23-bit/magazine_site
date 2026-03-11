# 🚀 БЫСТРЫЙ ЗАПУСК - РЫБНЫЙ ДЕНЬ

## Как запустить сайт (1 команда)

### Windows PowerShell
```powershell
Set-Location "c:\Users\Andrey\Documents\GitHub\magazine_site\admin_panel"; python manage.py runserver
```

### Windows CMD
```cmd
cd c:\Users\Andrey\Documents\GitHub\magazine_site\admin_panel && python manage.py runserver
```

### Или двойной клик
Двойной клик на файл: `RUN_COMPLETE_SITE.bat`

---

## Готово!

Откройте браузер: **http://localhost:8000**

Вы видите магазин Рыбный День! 🎣

---

## Что работает?

✅ Главная страница с товарами  
✅ Добавление в корзину  
✅ Редактирование веса (вручную и кнопками)  
✅ Оформление заказа  
✅ Email уведомления (если настроена почта)  

---

## Email (опционально)

Если хотите чтобы приходили письма:

1. Откройте: `admin_panel/fish_day_admin/settings.py`
2. Найдите строку: `EMAIL_HOST_PASSWORD = 'example-app-password'`
3. Получите пароль приложения Яндекса или Gmail
4. Замените значение на реальный пароль
5. Перезагрузите сервер

---

## Проблемы?

**Ошибка "не найдено"**
```
Убедитесь что находитесь в папке: admin_panel
Проверьте Python: python --version
```

**Порт 8000 занят**
```
python manage.py runserver 0.0.0.0:9000
# Потом откройте http://localhost:9000
```

**Стили не загружаются**
```
Нажмите Ctrl+Shift+R в браузере (жесткий кэш)
```

---

**Версия:** 1.0  
**Статус:** ✅ READY
