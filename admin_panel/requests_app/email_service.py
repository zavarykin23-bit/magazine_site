from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging
import smtplib

logger = logging.getLogger(__name__)


def _log_smtp_auth_hint(error):
    host = (getattr(settings, 'EMAIL_HOST', '') or '').strip().lower()
    user = (getattr(settings, 'EMAIL_HOST_USER', '') or '').strip().lower()
    password_set = bool((getattr(settings, 'EMAIL_HOST_PASSWORD', '') or '').strip())

    logger.error(
        "SMTP auth failed (host=%s, user=%s, ssl=%s, tls=%s, password_set=%s): %s",
        host,
        user,
        getattr(settings, 'EMAIL_USE_SSL', None),
        getattr(settings, 'EMAIL_USE_TLS', None),
        password_set,
        error,
    )

    if not user or not password_set:
        logger.error("EMAIL_HOST_USER/EMAIL_HOST_PASSWORD not set or empty.")
        return

    if user.endswith(('@mail.ru', '@inbox.ru', '@bk.ru', '@list.ru', '@internet.ru')):
        logger.error("Mail.ru config: EMAIL_HOST=smtp.mail.ru, EMAIL_PORT=465, EMAIL_USE_SSL=True, EMAIL_USE_TLS=False.")
    elif user.endswith(('@yandex.ru', '@ya.ru', '@yandex.com')):
        logger.error("Yandex config: EMAIL_HOST=smtp.yandex.ru, EMAIL_PORT=465, EMAIL_USE_SSL=True, EMAIL_USE_TLS=False.")
        logger.error("Use an app password from Yandex ID (regular account password may be rejected).")
    elif user.endswith(('@gmail.com', '@googlemail.com')):
        logger.error("Gmail config: EMAIL_HOST=smtp.gmail.com, EMAIL_PORT=587, EMAIL_USE_TLS=True, EMAIL_USE_SSL=False.")
        logger.error("Use an app password from Google Account (regular password is rejected).")


def send_order_confirmation_email(customer_data, cart_items, total_amount):
    """
    Отправить уведомление об оформлении заказа КЛИЕНТУ
    
    Args:
        customer_data (dict): Данные клиента {name, phone, email, address, comment}
        cart_items (list): Список товаров в формате JSON
        total_amount (str): Общая сумма заказа
    """
    
    if not customer_data.get('email'):
        logger.warning(f"Клиент {customer_data.get('name')} не указал email")
        return False
    
    customer_email = customer_data['email'].strip()
    
    try:
        subject = "Ваш заказ принят! Рыбный день"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    
                    <!-- Заголовок -->
                    <div style="text-align: center; border-bottom: 3px solid #7E4F35; padding-bottom: 20px; margin-bottom: 20px;">
                        <h1 style="color: #7E4F35; margin: 0;">🐟 Рыбный день</h1>
                        <p style="color: #666; margin: 5px 0 0 0;">Спасибо за вашу покупку!</p>
                    </div>
                    
                    <!-- Основное сообщение -->
                    <div style="margin-bottom: 20px;">
                        <p>Здравствуйте, <strong>{customer_data.get('name', 'Уважаемый клиент')}!</strong></p>
                        <p>Мы получили ваш заказ и начали его обработку. Менеджер свяжется с вами в ближайшее время для подтверждения деталей.</p>
                    </div>
                    
                    <!-- Детали заказа -->
                    <div style="background-color: #f8f5f0; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="color: #592A0F; margin-top: 0;">📋 Детали заказа</h3>
                        
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px 0; color: #666;">Ваше имя:</td>
                                <td style="padding: 10px 0; text-align: right; font-weight: bold;">{customer_data.get('name')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px 0; color: #666;">Телефон:</td>
                                <td style="padding: 10px 0; text-align: right; font-weight: bold;">{customer_data.get('phone')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px 0; color: #666;">Email:</td>
                                <td style="padding: 10px 0; text-align: right; font-weight: bold;">{customer_email}</td>
                            </tr>
        """
        
        if customer_data.get('address'):
            html_message += f"""
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px 0; color: #666;">Адрес доставки:</td>
                                <td style="padding: 10px 0; text-align: right; font-weight: bold;">{customer_data.get('address')}</td>
                            </tr>
            """
        
        html_message += """
                        </table>
                    </div>
                    
                    <!-- Товары в заказе -->
                    <div style="margin-bottom: 20px;">
                        <h3 style="color: #592A0F; margin-top: 0;">🛒 Ваши товары</h3>
                        <table style="width: 100%; border-collapse: collapse;">
        """
        
        if isinstance(cart_items, str):
            html_message += f"""
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd; color: #666;">
                                    {cart_items.replace(chr(10), '<br>')}
                                </td>
                            </tr>
            """
        else:
            for item in cart_items:
                html_message += f"""
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px; color: #666;">{item.get('name', 'Товар')}</td>
                                <td style="padding: 10px; text-align: right; color: #666;">{item.get('amount', 0)} {item.get('unit', 'шт')}</td>
                                <td style="padding: 10px; text-align: right; color: #666;">{item.get('price', 0)} ₽</td>
                                <td style="padding: 10px; text-align: right; font-weight: bold; color: #7E4F35;">{item.get('total', 0)} ₽</td>
                            </tr>
                """
        
        html_message += f"""
                        </table>
                    </div>
                    
                    <!-- Итоговая сумма -->
                    <div style="background-color: #592A0F; color: white; padding: 15px; border-radius: 5px; text-align: right; margin-bottom: 20px;">
                        <h2 style="margin: 0; font-size: 24px;">Итого: <span style="color: #FFD700;">{total_amount}</span> ₽</h2>
                    </div>
                    
                    <!-- Дополнительная информация -->
                    <div style="background-color: #f0e6d2; padding: 15px; border-left: 4px solid #B59B76; margin-bottom: 20px;">
                        <p style="margin: 0; color: #592A0F;"><strong>⏱️ Что дальше?</strong></p>
                        <ul style="margin: 10px 0 0 0; padding-left: 20px; color: #666;">
                            <li>Менеджер свяжется с вами в течение 1-2 часов</li>
                            <li>Мы уточним детали доставки</li>
                            <li>Если заказ более 5000₽ - доставка бесплатна!</li>
                            <li>Оплата наличными или по переводу</li>
                        </ul>
                    </div>
        """
        
        if customer_data.get('comment'):
            html_message += f"""
                    <!-- Комментарий клиента -->
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <p style="margin: 0 0 10px 0; color: #666;"><strong>💬 Ваш комментарий:</strong></p>
                        <p style="margin: 0; color: #666; font-style: italic;">"{customer_data.get('comment')}"</p>
                    </div>
            """
        
        html_message += """
                    <!-- Контакты -->
                    <div style="border-top: 1px solid #ddd; padding-top: 20px; text-align: center; color: #666; font-size: 12px;">
                        <p style="margin: 5px 0;">
                            <strong>🐟 Рыбный день</strong><br>
                            Магазин деликатесов и закусок
                        </p>
                        <p style="margin: 5px 0;">
                            📞 +7 (XXX) XXX-XX-XX<br>
                            📧 support@fishday.ru
                        </p>
                        <p style="margin: 5px 0; color: #999;">
                            Это автоматическое письмо, не отвечайте на него.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Заказ #{customer_data.get('name')} принят",
            from_email=settings.EMAIL_HOST_USER,
            to=[customer_email]
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        
        logger.info(f"✅ Письмо клиенту отправлено на {customer_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        _log_smtp_auth_hint(e)
        logger.error(f"SMTP auth error: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке письма клиенту: {str(e)}", exc_info=True)
        return False


def send_order_notification_to_admin(customer_data, cart_items, total_amount):
    """
    Отправить уведомление об оформлении заказа АДМИНИСТРАТОРУ
    
    Args:
        customer_data (dict): Данные клиента
        cart_items (list): Список товаров
        total_amount (str): Общая сумма заказа
    """
    
    try:
        subject = f"🔔 Новый заказ от {customer_data.get('name')}"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 700px; margin: 0 auto; background-color: #fff3cd; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #7E4F35; margin-top: 0;">🔔 НОВЫЙ ЗАКАЗ В СИСТЕМЕ</h2>
                    
                    <div style="background-color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="color: #592A0F;">👤 Данные клиента:</h3>
                        <p><strong>Имя:</strong> {customer_data.get('name')}</p>
                        <p><strong>Телефон:</strong> {customer_data.get('phone')}</p>
                        <p><strong>Email:</strong> {customer_data.get('email', 'Не указан')}</p>
                        <p><strong>Адрес:</strong> {customer_data.get('address', 'Не указан')}</p>
                        <p><strong>Комментарий:</strong> {customer_data.get('comment', 'Нет')}</p>
                    </div>
                    
                    <div style="background-color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="color: #592A0F;">📦 Товары:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
        """
        
        if isinstance(cart_items, str):
            html_message += f"""
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                    {cart_items.replace(chr(10), '<br>')}
                                </td>
                            </tr>
            """
        else:
            for item in cart_items:
                html_message += f"""
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px;">{item.get('name', 'Товар')}</td>
                                <td style="padding: 10px; text-align: right;">{item.get('amount', 0)} {item.get('unit', 'шт')}</td>
                                <td style="padding: 10px; text-align: right;">{item.get('price', 0)} ₽</td>
                                <td style="padding: 10px; text-align: right; font-weight: bold;">{item.get('total', 0)} ₽</td>
                            </tr>
                """
        
        html_message += f"""
                        </table>
                    </div>
                    
                    <div style="background-color: #592A0F; color: white; padding: 15px; border-radius: 5px; text-align: right; margin-bottom: 20px;">
                        <h2 style="margin: 0;">Всего: {total_amount} ₽</h2>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="http://localhost:8000/admin/" style="background-color: #7E4F35; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Открыть админ-панель
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Новый заказ от {customer_data.get('name')}",
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.ADMIN_EMAIL]
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        
        logger.info(f"✅ Письмо администратору отправлено на {settings.ADMIN_EMAIL}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        _log_smtp_auth_hint(e)
        logger.error(f"SMTP auth error: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке письма администратору: {str(e)}", exc_info=True)
        return False


def send_test_email(recipient_email):
    """
    Отправить тестовое письмо для проверки конфигурации
    
    Args:
        recipient_email (str): Email получателя
    """
    try:
        subject = "Тестовое письмо - Рыбный день"
        html_message = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #7E4F35;">✅ Конфигурация email работает!</h2>
                    <p>Это тестовое письмо подтверждает, что система отправки писем настроена правильно.</p>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Рыбный день - магазин деликатесов
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body="Тестовое письмо",
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email]
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        
        logger.info(f"✅ Тестовое письмо отправлено на {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        _log_smtp_auth_hint(e)
        logger.error(f"SMTP auth error: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке тестового письма: {str(e)}", exc_info=True)
        return False
