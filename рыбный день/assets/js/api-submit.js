/**
 * Скрипт для отправки заявок на backend (Django админ-панель)
 * Используется для: заказов, обратных звонков, консультаций
 */

// URL api endpoint (измените на ваш адрес)
const API_URL = 'http://localhost:8000/api/submit-request/';

// Класс для работы с формами
class FormSubmitter {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.apiUrl = options.apiUrl || API_URL;
        this.successCallback = options.onSuccess || null;
        this.errorCallback = options.onError || null;
        
        this.initForm();
    }
    
    initForm() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    
    /**
     * Обработка отправки формы
     */
    async handleSubmit(event) {
        event.preventDefault();
        
        // Проверка honeypot (защита от спама)
        const honeypot = this.form.querySelector('[name="honeypot"]');
        if (honeypot && honeypot.value.trim() !== '') {
            console.warn('Honeypot field filled - possible spam');
            this.showMessage('Спасибо! Заявка отправлена.', 'success');
            this.form.reset();
            return;
        }
        
        // Сбор данных формы
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData);
        
        // Валидация
        if (!this.validate(data)) {
            return;
        }
        
        // Отправка
        try {
            this.showLoading(true);
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.showMessage(result.message, 'success');
                this.form.reset();
                if (this.successCallback) {
                    this.successCallback(result);
                }
            } else {
                this.showMessage(result.message, 'error');
                if (this.errorCallback) {
                    this.errorCallback(result);
                }
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            this.showMessage('Ошибка при отправке. Попробуйте позже.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * Валидация данных
     */
    validate(data) {
        if (!data.name || !data.name.trim()) {
            this.showMessage('Пожалуйста, введите имя', 'error');
            return false;
        }
        
        if (!data.phone || !data.phone.trim()) {
            this.showMessage('Пожалуйста, введите номер телефона', 'error');
            return false;
        }
        
        // Проверка телефона (минимально: должны быть цифры)
        if (!/\d{6,}/.test(data.phone)) {
            this.showMessage('Неверный номер телефона', 'error');
            return false;
        }
        
        if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            this.showMessage('Неверный email', 'error');
            return false;
        }
        
        return true;
    }
    
    /**
     * Показать сообщение
     */
    showMessage(message, type = 'info') {
        // Удалить старое сообщение
        const oldMessage = this.form.querySelector('.form-message');
        if (oldMessage) {
            oldMessage.remove();
        }
        
        // Создать новое сообщение
        const messageEl = document.createElement('div');
        messageEl.className = `form-message form-message-${type}`;
        messageEl.textContent = message;
        
        this.form.insertBefore(messageEl, this.form.firstChild);
        
        // Автоматически удалить через 5 секунд
        setTimeout(() => {
            messageEl.style.opacity = '0';
            setTimeout(() => messageEl.remove(), 300);
        }, 5000);
    }
    
    /**
     * Показать/скрыть загрузку
     */
    showLoading(show) {
        const submitBtn = this.form.querySelector('button[type="submit"]');
        if (!submitBtn) return;
        
        if (show) {
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Отправка...';
        } else {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
        }
    }
}

/**
 * Инициализация всех форм на странице
 */
document.addEventListener('DOMContentLoaded', () => {
    // Формы заказа
    const orderForms = document.querySelectorAll('[data-form-type="order"]');
    orderForms.forEach(form => {
        new FormSubmitter(form, {
            onSuccess: () => {
                // После успешной отправки заказа
                console.log('Заказ успешно отправлен');
            }
        });
    });
    
    // Формы обратного звонка
    const callbackForms = document.querySelectorAll('[data-form-type="callback"]');
    callbackForms.forEach(form => {
        new FormSubmitter(form);
    });
    
    // Общие формы
    const generalForms = document.querySelectorAll('form[data-submit-api]');
    generalForms.forEach(form => {
        const apiUrl = form.dataset.submitApi;
        new FormSubmitter(form, { apiUrl });
    });
});

// Экспорт для использования в других скриптах
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormSubmitter;
}
