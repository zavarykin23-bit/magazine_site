# -*- coding: utf-8 -*-
"""
Модели для хранения заявок и заказов
"""
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class CustomerRequest(models.Model):
    """
    Модель для хранения заявок от клиентов
    (заказы товаров, обратные звонки, консультации и т.д.)
    """
    
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('called', 'Звонили'),
        ('waiting', 'Ожидание'),
        ('processing', 'Обработка'),
        ('completed', 'Завершена'),
        ('rejected', 'Отклонена'),
        ('spam', 'Спам'),
    )
    
    REQUEST_TYPE_CHOICES = (
        ('order', 'Заказ товара'),
        ('callback', 'Обратный звонок'),
        ('consultation', 'Консультация'),
        ('question', 'Вопрос'),
        ('complaint', 'Жалоба'),
    )
    
    # Основные данные клиента
    name = models.CharField(
        max_length=200,
        verbose_name='Имя клиента'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Введите корректный номер телефона'
        )]
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=True,
        null=True
    )
    
    # Информация о заявке
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default='order',
        verbose_name='Тип заявки'
    )
    product_name = models.CharField(
        max_length=300,
        verbose_name='Название товара',
        blank=True,
        null=True
    )
    product_weight = models.CharField(
        max_length=100,
        verbose_name='Вес/Количество',
        blank=True,
        null=True,
        help_text='Например: 1 кг, 500 г, 2 шт'
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name='Количество товара'
    )
    
    # Доставка
    address = models.TextField(
        verbose_name='Адрес доставки',
        blank=True,
        null=True
    )
    
    # Коммент
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
        help_text='Дополнительная информация от клиента'
    )
    
    # Статус и отслеживание
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
        db_index=True
    )
    
    # Временные метки
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    # Служебные поля
    ip_address = models.GenericIPAddressField(
        verbose_name='IP адрес',
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        verbose_name='User Agent',
        blank=True,
        null=True
    )
    
    # Honeypot для защиты от спама
    honeypot = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Honeypot (для спам-фильтра)'
    )

    # Подробности заказа (может содержать несколько товаров в виде JSON).
    # Раньше существовали только поля product_name/product_weight/quantity,
    # которые годились лишь для одного товара. Добавляем отдельное поле, чтобы
    # сохранять полный список позиций и видеть его в админке.
    order_details = models.TextField(
        verbose_name='Детали заказа (JSON)',
        blank=True,
        null=True,
        help_text='JSON с полным содержимым корзины - каждый товар с именем, ценой, количеством'
    )
    
    # Общая сумма заказа
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма заказа',
        blank=True,
        null=True,
        default=0.00
    )
    
    notes = models.TextField(
        verbose_name='Заметки администратора',
        blank=True,
        null=True,
        help_text='Личные заметки о заявке'
    )
    
    class Meta:
        verbose_name = 'Заявка клиента'
        verbose_name_plural = 'Заявки клиентов'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_request_type_display()} ({self.created_at.strftime('%d.%m.%Y')})"
    
    @property
    def get_status_display_ru(self):
        """Получить русское название статуса"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def get_order_items_list(self):
        """Получить список товаров из JSON"""
        if not self.order_details:
            return []
        
        import json
        try:
            data = json.loads(self.order_details)
            # Если это список (массив товаров)
            if isinstance(data, list):
                return data
            # Если это словарь с ключом 'cart' или 'items'
            elif isinstance(data, dict):
                return data.get('cart', data.get('items', []))
            return []
        except json.JSONDecodeError:
            return []
    
    def get_order_html(self):
        """Получить красивый HTML таблицы товаров для админки"""
        items = self.get_order_items_list()
        if not items:
            return '<p style="color: #999;">Нет информации о товарах</p>'
        
        html = '<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">'
        html += '<thead><tr style="background-color: #f0f0f0; border-bottom: 2px solid #ddd;">'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Товар</th>'
        html += '<th style="padding: 8px; text-align: center; border: 1px solid #ddd;">Цена</th>'
        html += '<th style="padding: 8px; text-align: center; border: 1px solid #ddd;">Кол-во / Вес</th>'
        html += '<th style="padding: 8px; text-align: right; border: 1px solid #ddd;">Сумма</th>'
        html += '</tr></thead><tbody>'
        
        for item in items:
            name = item.get('name', 'Неизвестный товар')
            price = item.get('price', 0)
            
            # Поддержка разных форматов данных
            amount = item.get('amount') or item.get('quantity', 1)
            unit = item.get('unit', 'шт')  # 'кг', 'шт', 'г' и т.д.
            total_price = item.get('total') or item.get('totalPrice', 0)
            
            # Форматируем количество с единицей измерения
            quantity_text = f"{amount} {unit}"
            
            html += f'<tr style="border-bottom: 1px solid #eee;">'
            html += f'<td style="padding: 8px; border: 1px solid #ddd;">{name}</td>'
            html += f'<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">{price}₽</td>'
            html += f'<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">{quantity_text}</td>'
            html += f'<td style="padding: 8px; text-align: right; border: 1px solid #ddd; font-weight: bold;">{total_price}₽</td>'
            html += f'</tr>'
        
        html += '</tbody></table>'
        
        if self.order_total:
            html += f'<div style="margin-top: 10px; text-align: right; font-size: 14px; font-weight: bold;">'
            html += f'Итого: <span style="color: #FF6B6B; font-size: 16px;">{self.order_total}₽</span>'
            html += f'</div>'
        
        return html


class AdminLog(models.Model):
    """
    Логирование действий администратора для отслеживания
    """
    ACTION_CHOICES = (
        ('view', 'Просмотр'),
        ('edit', 'Редактирование'),
        ('status_change', 'Изменение статуса'),
        ('delete', 'Удаление'),
        ('export', 'Экспорт'),
    )
    
    admin_user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Администратор'
    )
    request = models.ForeignKey(
        CustomerRequest,
        on_delete=models.CASCADE,
        verbose_name='Заявка'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Действие'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время'
    )
    
    class Meta:
        verbose_name = 'Лог администратора'
        verbose_name_plural = 'Логи администратора'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.admin_user} - {self.get_action_display()} - {self.request.name}"
