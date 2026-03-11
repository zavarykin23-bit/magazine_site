# -*- coding: utf-8 -*-
"""
Конфигурация Django администратора для приложения
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from .models import CustomerRequest, AdminLog


@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления заявками
    """
    
    # Отображаемые поля в списке
    list_display = [
        'name_display',
        'phone',
        'request_type_display',
        'product_name_short',
        'status_colored',
        'created_at_display',
        'actions_display'
    ]
    
    # Фильтры
    list_filter = [
        'status',
        'request_type',
        'created_at',
        'email',
    ]
    
    # Поиск
    search_fields = [
        'name',
        'phone',
        'email',
        'product_name',
        'comment'
    ]
    
    # Редактирование
    fieldsets = (
        ('📋 Основная информация', {
            'fields': ('name', 'phone', 'email', 'request_type')
        }),
        ('🛍️ Информация о товаре', {
            'fields': ('product_name', 'product_weight', 'quantity'),
            'classes': ('collapse',)
        }),
        ('📝 Полная корзина', {
            'fields': ('order_details_display', 'order_total'),
            'description': 'Красивое отображение товаров из заказа'
        }),
        ('📍 Доставка', {
            'fields': ('address',),
            'classes': ('collapse',)
        }),
        ('💬 Сообщение', {
            'fields': ('comment',)
        }),
        ('📊 Статус и управление', {
            'fields': ('status', 'notes'),
            'classes': ('collapse',)
        }),
        ('🔒 Служебная информация', {
            'fields': ('ip_address', 'user_agent', 'honeypot', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Автоматически заполняется системой'
        }),
    )
    
    # Только для чтения
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'honeypot', 'order_details_display']
    
    # Сортировка по умолчанию
    ordering = ['-created_at']
    
    # Количество элементов на странице
    list_per_page = 50
    
    # Действия
    actions = ['mark_as_called', 'mark_as_processing', 'mark_as_completed', 'mark_as_rejected', 'export_to_csv']
    
    def name_display(self, obj):
        """Отображение имени с иконкой"""
        return f"👤 {obj.name}"
    name_display.short_description = "Имя"
    
    def product_name_short(self, obj):
        """Укороченное название товара"""
        if obj.product_name:
            name = obj.product_name[:40]
            if len(obj.product_name) > 40:
                name += '...'
            return name
        return '—'
    product_name_short.short_description = "Товар"
    
    def request_type_display(self, obj):
        """Тип заявки с иконками"""
        icons = {
            'order': '🛒',
            'callback': '📞',
            'consultation': '💭',
            'question': '❓',
            'complaint': '⚠️'
        }
        icon = icons.get(obj.request_type, '')
        return f"{icon} {obj.get_request_type_display()}"
    request_type_display.short_description = "Тип"
    
    def status_colored(self, obj):
        """Статус с цветом"""
        colors = {
            'new': '#FF6B6B',  # красный
            'called': '#FFA500',  # оранжевый
            'waiting': '#FFD93D',  # жёлтый
            'processing': '#6BCB77',  # зелёный
            'completed': '#4D96FF',  # синий
            'rejected': '#808080',  # серый
            'spam': '#000000'  # чёрный
        }
        color = colors.get(obj.status, '#999999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"
    
    def created_at_display(self, obj):
        """Дата создания с временем"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at_display.short_description = "Дата"
    
    def actions_display(self, obj):
        """Быстрые действия"""
        return format_html(
            '<a class="button" href="{}">Открыть</a>',
            reverse('admin:requests_app_customerrequest_change', args=[obj.pk])
        )
    actions_display.short_description = "Действия"
    
    def order_details_display(self, obj):
        """Красиво отображаем таблицу товаров"""
        return format_html(obj.get_order_html())
    order_details_display.short_description = "🛒 Товары в заказе"
    
    # Массовые действия
    def mark_as_called(self, request, queryset):
        """Отметить как 'Звонили'"""
        updated = queryset.update(status='called')
        self.message_user(request, f'✅ Обновлено {updated} заявок')
    mark_as_called.short_description = "Отметить как 'Звонили'"
    
    def mark_as_processing(self, request, queryset):
        """Отметить как 'Обработка'"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'✅ Обновлено {updated} заявок')
    mark_as_processing.short_description = "Отметить как 'Обработка'"
    
    def mark_as_completed(self, request, queryset):
        """Отметить как 'Завершена'"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'✅ Обновлено {updated} заявок')
    mark_as_completed.short_description = "Отметить как 'Завершена'"
    
    def mark_as_rejected(self, request, queryset):
        """Отметить как 'Отклонена'"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'✅ Обновлено {updated} заявок')
    mark_as_rejected.short_description = "Отметить как 'Отклонена'"
    
    def export_to_csv(self, request, queryset):
        """Экспортировать в CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="requests.csv"'
        
        # BOM для правильного отображения кириллицы в Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        writer.writerow([
            'Имя', 'Телефон', 'Email', 'Тип', 'Товар', 'Вес', 
            'Адрес', 'Комментарий', 'Детали заказа', 'Статус', 'Дата создания'
        ])
        
        for req in queryset:
            writer.writerow([
                req.name,
                req.phone,
                req.email or '',
                req.get_request_type_display(),
                req.product_name or '',
                req.product_weight or '',
                req.address or '',
                req.comment or '',
                req.order_details or '',
                req.get_status_display(),
                req.created_at.strftime('%d.%m.%Y %H:%M')
            ])
        
        return response
    export_to_csv.short_description = "📥 Экспортировать в CSV"


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    """
    Логирование действий администратора
    """
    list_display = ['admin_user', 'action', 'request', 'timestamp']
    list_filter = ['action', 'timestamp', 'admin_user']
    search_fields = ['request__name', 'request__phone', 'description']
    readonly_fields = ['admin_user', 'request', 'action', 'description', 'timestamp']
    
    def has_add_permission(self, request):
        """Запретить ручное добавление логов"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Запретить удаление логов (для аудита)"""
        return False


# Кастомизация заголовка админки
admin.site.site_header = "🐟 FISH DAY - Администраторская панель"
admin.site.site_title = "FISH DAY Admin"
admin.site.index_title = "Добро пожаловать в админку FISH DAY"
