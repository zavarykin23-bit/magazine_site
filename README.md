# 🎣 Рыбный День - Fish Day Shop

**Полнофункциональный интернет-магазин для продажи рыбы и снеков**

![Status](https://img.shields.io/badge/Status-COMPLETE-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Django](https://img.shields.io/badge/Django-4.2-darkgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Документация

Для быстрого старта - смотрите:
1. **[QUICK_START.md](./QUICK_START.md)** ⚡ - 5 минут для запуска
2. **[COMPLETE_SETUP_GUIDE.md](./COMPLETE_SETUP_GUIDE.md)** 📋 - Полное руководство
3. **[ARCHITECTURE_AND_INTEGRATION.md](./ARCHITECTURE_AND_INTEGRATION.md)** 🏗️ - Архитектура проекта
4. **[FINAL_STATUS.md](./FINAL_STATUS.md)** ✅ - Статус всех функций

---

## 🚀 Быстрый старт

### Запуск (3 команды)

```powershell
# 1. Перейти в папку
Set-Location "c:\Users\Andrey\Documents\GitHub\magazine_site\admin_panel"

# 2. Запустить сервер
python manage.py runserver

# 3. Открыть браузер на http://localhost:8000
```

Готово! Сайт работает! 🎉

---

## ✨ Функциональность

### Для покупателей 👥
- ✅ Просмотр каталога товаров
- ✅ Добавление товаров в корзину
- ✅ Редактирование веса/количества (вручную и кнопками)
- ✅ Оформление заказа
- ✅ Email подтверждение заказа
- ✅ Поиск товаров

### Для администратора 👨‍💼
- ✅ Admin панель `/admin/`
- ✅ Просмотр всех заказов
- ✅ Email уведомления о новых заказах
- ✅ Статистика заказов

### Технология 🔧
- ✅ Современный фронтенд (HTML5, CSS3, JavaScript)
- ✅ Django 4.2 бэкенд
- ✅ REST API для взаимодействия
- ✅ SQLite база данных
- ✅ Email система (SMTP)
- ✅ Валидация формы
- ✅ Обработка ошибок

---

## 📁 Структура

```
magazine_site/
├── 📄 QUICK_START.md                    ← Начните отсюда!
├── 📄 COMPLETE_SETUP_GUIDE.md          ← Полное руководство
├── 📄 ARCHITECTURE_AND_INTEGRATION.md  ← Как все работает
├── 📄 FINAL_STATUS.md                  ← Статус функций
│
├── 📂 рыбный день/                     ← Фронтенд (HTML/CSS/JS)
│   ├── index.html                      ← Главная страница
│   ├── cart.html                       ← Корзина
│   └── assets/                         ← CSS, JS, Images
│
└── 📂 admin_panel/                     ← Бэкенд (Django)
    ├── manage.py                       ← Управление Django
    ├── db.sqlite3                      ← База данных
    ├── RUN_COMPLETE_SITE.bat           ← Запуск на Windows
    ├── fish_day_admin/                 ← Конфигурация
    │   ├── settings.py                 ← Параметры (EMAIL, БД)
    │   └── urls.py                     ← Маршруты
    └── requests_app/                   ← Приложение заказов
        ├── views.py                    ← API обработчики
        ├── email_service.py            ← Email функции
        └── models.py                   ← Модель БД
```

---

## 🔧 Требования

- Python 3.8+
- Django 4.2+
- Windows/Mac/Linux

## 📦 Установка зависимостей

```powershell
cd admin_panel
pip install -r requirements.txt
```

---

## 🌐 URLs

| URL | Описание |
|-----|---------|
| `http://localhost:8000` | Главная страница (каталог) |
| `http://localhost:8000/cart.html` | Корзина |
| `http://localhost:8000/api/` | API документация |
| `http://localhost:8000/admin/` | Admin панель |
| `http://localhost:8000/api/submit-request/` | Отправить заказ (POST) |

---

## 📧 Email система

Поддерживаются:
- **Яндекс Почта** (smtp.yandex.ru) - рекомендуется
- **Gmail** (smtp.gmail.com) - альтернатива

Все письма отправляются на `fishday068@mail.ru`

Подробнее: смотрите `COMPLETE_SETUP_GUIDE.md` раздел "Email"

---

## 🐛 Исправления в проекте

- ✅ Поле ввода веса теперь редактируемое (было readonly)
- ✅ Плавающая точка при расчетах (使用 integer math)
- ✅ Единый Django сервер для фронтенда и API (не нужны два сервера)
- ✅ Правильное обслуживание статических файлов (CSS, JS, Images)

---

## 🚀 Примеры использования

### Добавить товар в каталог

Отредактируйте файл `рыбный день/index.html`, найдите секцию товаров и добавьте:

```html
<div class="product">
    <img src="assets/images/my-fish.png" alt="Моя рыба">
    <h3>Моя рыба</h3>
    <p>500 ₽/кг</p>
</div>
```

### Проверить заказы

```powershell
cd admin_panel
python manage.py shell
```

```python
from requests_app.models import CustomerRequest
for order in CustomerRequest.objects.all():
    print(f"{order.name} - {order.phone} - {order.total}₽")
```

### Отправить тестовое письмо

```python
from requests_app.email_service import send_test_email
send_test_email('your@email.com')
```

---

## 📊 Статистика заказов

Все заказы автоматически сохраняются в БД:
- 📝 Имя и контакты клиента
- 📦 Список товаров с ценами
- 💰 Общая сумма заказа
- ⏰ Время создания заказа
- 🌐 IP адрес клиента

Просмотрите через Admin панель: `/admin/`

---

## ⚙️ Конфигурация

### Изменить порт

```powershell
python manage.py runserver 0.0.0.0:9000
```

### Отключить Debug режим

Отредактируйте `admin_panel/fish_day_admin/settings.py`:

```python
DEBUG = False  # Включить для Production
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Подключить PostgreSQL

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fish_day',
        'USER': 'postgres',
        'PASSWORD': '...',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🔐 Безопасность

- ✅ Валидация всех входных данных
- ✅ CSRF защита (Django)
- ✅ Email подтверждение для админа
- ✅ Honeypot поле от спама
- ✅ IP логирование заказов

---

## 🎯 TODO для Production

- [ ] Отключить DEBUG режим
- [ ] Настроить HTTPS
- [ ] Использовать PostgreSQL
- [ ] Настроить бэкап БД
- [ ] Настроить мониторинг
- [ ] Добавить аутентификацию
- [ ] Настроить CDN для ассетов

---

## 📞 Контакты

**Email:** fishday068@mail.ru

**Проект:** Fish Day Shop (Рыбный день)

---

## 📄 Лицензия

MIT License - свободное использование в личных и коммерческих целях.

---

## 🙏 Спасибо за использование!

**Проект полностью готов к работе!** 🎉

Все функции реализованы и протестированы.
Просто запустите `python manage.py runserver` и начните продавать! 🎣

---

**Версия:** 1.0.0  
**Дата:** March 2026  
**Статус:** ✅ COMPLETE
