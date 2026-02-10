// DOM элементы
const cartItemsContainer = document.getElementById('cartItems');
const subtotalElement = document.getElementById('subtotal');
const totalElement = document.getElementById('total');
const checkoutBtn = document.getElementById('checkoutBtn');
const orderModal = document.getElementById('orderModal');
const closeModal = document.getElementById('closeModal');
const orderForm = document.getElementById('orderForm');

// Получение корзины из localStorage
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Функция для отображения товаров в корзине
function displayCartItems() {
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <h3>Корзина пуста</h3>
                <p>Добавьте товары из прейскуранта</p>
            </div>
        `;
        return;
    }
    
    cartItemsContainer.innerHTML = cart.map((item, index) => `
        <div class="cart-item" data-index="${index}">
            <div class="cart-item-image">
                <img src="${item.image}" alt="${item.name}">
            </div>
            
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p class="cart-item-price">
                    ${item.price}₽ ${item.type === 'weight' ? '/ кг' : '/ шт'}
                </p>
                ${item.type === 'weight' && item.customWeight ? 
                    `<p class="cart-item-weight">Вес: ${item.customWeight} кг</p>` : 
                    `<p class="cart-item-quantity">Количество: ${item.quantity} шт</p>`}
            </div>
            
            <div class="cart-item-total">
                <p>${item.totalPrice}₽</p>
            </div>
            
            <div class="cart-item-actions">
                <button class="cart-item-remove" data-index="${index}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    // Добавляем обработчики для кнопок удаления
    document.querySelectorAll('.cart-item-remove').forEach(button => {
        button.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-index'));
            removeFromCart(index);
        });
    });
    
    updateCartTotal();
}

// Функция для удаления товара из корзины
function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems();
    updateCartCount();
}

// Функция для обновления общей суммы
function updateCartTotal() {
    const subtotal = cart.reduce((total, item) => {
        return total + parseFloat(item.totalPrice);
    }, 0);
    
    subtotalElement.textContent = subtotal.toFixed(2) + '₽';
    totalElement.textContent = subtotal.toFixed(2) + '₽';
}

// Открытие модального окна оформления заказа
checkoutBtn.addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Добавьте товары в корзину перед оформлением заказа');
        return;
    }
    
    orderModal.style.display = 'flex';
});

// Закрытие модального окна
closeModal.addEventListener('click', () => {
    orderModal.style.display = 'none';
});

// Закрытие модального окна при клике на оверлей
orderModal.addEventListener('click', (e) => {
    if (e.target === orderModal) {
        orderModal.style.display = 'none';
    }
});

// Обработка отправки формы заказа
orderForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Сбор данных формы
    const formData = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value || 'Не указан',
        address: document.getElementById('address').value || 'Не указан',
        comment: document.getElementById('comment').value || 'Нет комментария',
        cart: cart,
        total: totalElement.textContent,
        date: new Date().toLocaleString('ru-RU')
    };
    
    // В реальном проекте здесь будет отправка на сервер
    // Для примера имитируем отправку
    
    try {
        // Здесь должен быть реальный код отправки на email через сервер
        // Например, через Formspree, EmailJS или собственный бэкенд
        
        // Временно сохраняем заказ в localStorage для демонстрации
        const orders = JSON.parse(localStorage.getItem('orders')) || [];
        orders.push(formData);
        localStorage.setItem('orders', JSON.stringify(orders));
        
        // Очищаем корзину
        cart = [];
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        displayCartItems();
        
        // Закрываем модальное окно
        orderModal.style.display = 'none';
        
        // Показываем сообщение об успехе
        showSuccessMessage();
        
    } catch (error) {
        console.error('Ошибка при отправке заказа:', error);
        alert('Произошла ошибка при отправке заказа. Пожалуйста, попробуйте еще раз или позвоните нам.');
    }
});

// Функция для показа сообщения об успешном оформлении заказа
function showSuccessMessage() {
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.innerHTML = `
        <div class="success-content">
            <i class="fas fa-check-circle"></i>
            <h3>Заказ успешно оформлен!</h3>
            <p>Наш менеджер свяжется с вами в ближайшее время для уточнения деталей.</p>
            <p>Ожидайте звонка на указанный номер телефона.</p>
            <button class="btn" id="closeSuccess">Понятно</button>
        </div>
    `;
    
    successMessage.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    document.body.appendChild(successMessage);
    
    document.getElementById('closeSuccess').addEventListener('click', () => {
        successMessage.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => successMessage.remove(), 300);
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    displayCartItems();
    
    // Добавляем CSS анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        }
        
        .modal {
            background: white;
            border-radius: var(--border-radius);
            width: 90%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .modal-header {
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #666;
        }
        
        .modal-body {
            padding: 20px;
        }
        
        .modal-info {
            background: #f8f5f0;
            padding: 15px;
            border-radius: var(--border-radius);
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
        }
        
        .modal-info i {
            color: var(--primary-color);
            margin-right: 10px;
            margin-top: 3px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            font-family: 'Source Serif 4', serif;
            font-size: 1rem;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .checkbox-label input {
            width: auto;
            margin-right: 10px;
        }
        
        .cart-item {
            display: grid;
            grid-template-columns: 100px 1fr auto auto;
            gap: 20px;
            padding: 20px;
            border-bottom: 1px solid #eee;
            align-items: center;
        }
        
        .cart-item-image img {
            width: 100%;
            height: 80px;
            object-fit: cover;
            border-radius: 5px;
        }
        
        .cart-item-remove {
            background: none;
            border: none;
            color: #dc3545;
            cursor: pointer;
            font-size: 1.2rem;
        }
        
        .empty-cart {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        
        .empty-cart i {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #ddd;
        }
        
        .trust-note {
            background: #f8f5f0;
            padding: 15px;
            border-radius: var(--border-radius);
            margin: 20px 0;
            display: flex;
            align-items: center;
        }
        
        .trust-note i {
            color: var(--primary-color);
            margin-right: 10px;
            font-size: 1.5rem;
        }
    `;
    
    document.head.appendChild(style);
});