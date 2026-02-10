// Получение ID товара из URL
const urlParams = new URLSearchParams(window.location.search);
const productId = parseInt(urlParams.get('id'));

// Данные товаров (должны быть импортированы из products.js или храниться отдельно)
const products = []; // Здесь должны быть данные товаров

// Поиск товара по ID
const product = products.find(p => p.id === productId);

// DOM элементы
const productDetail = document.getElementById('productDetail');
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Функция для добавления товара в корзину
function addToCart(product, quantity, customWeight = null) {
    // Проверяем, есть ли уже такой товар в корзине
    const existingItemIndex = cart.findIndex(item => 
        item.id === product.id && 
        (product.type === 'piece' || item.customWeight === customWeight)
    );
    
    if (existingItemIndex > -1) {
        // Если товар уже есть, обновляем количество
        cart[existingItemIndex].quantity += quantity;
    } else {
        // Добавляем новый товар
        const cartItem = {
            id: product.id,
            name: product.name,
            price: product.price,
            type: product.type,
            quantity: quantity,
            customWeight: customWeight,
            image: product.image,
            totalPrice: product.type === 'weight' && customWeight 
                ? (product.price * customWeight).toFixed(2)
                : (product.price * quantity).toFixed(2)
        };
        
        cart.push(cartItem);
    }
    
    // Сохраняем в localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Обновляем счетчик корзины
    updateCartCount();
    
    // Показываем уведомление
    showNotification('Товар добавлен в корзину!');
}

// Функция для показа уведомления
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--success-color);
        color: white;
        padding: 15px 20px;
        border-radius: var(--border-radius);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Отображение информации о товаре
function displayProduct() {
    if (!product) {
        productDetail.innerHTML = `
            <div class="product-not-found">
                <h2>Товар не найден</h2>
                <p>Извините, запрашиваемый товар не существует.</p>
            </div>
        `;
        return;
    }
    
    productDetail.innerHTML = `
        <div class="product-main">
            <div class="product-image-large">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="product-info-large">
                <h1>${product.name}</h1>
                <p class="product-price-large">${product.price}₽ ${product.type === 'weight' ? '/ кг' : '/ шт'}</p>
                <p class="product-description-large">${product.description}</p>
                
                <div class="product-selector">
                    ${product.type === 'weight' ? `
                        <div class="weight-selector">
                            <label for="weight">Выберите вес (кг):</label>
                            <div class="weight-input-group">
                                <button class="weight-btn minus"><i class="fas fa-minus"></i></button>
                                <input type="number" id="weight" min="0.1" max="10" step="0.1" value="1" class="weight-input">
                                <button class="weight-btn plus"><i class="fas fa-plus"></i></button>
                            </div>
                            <p class="weight-price">Итого: <span id="totalPrice">${product.price}</span>₽</p>
                        </div>
                    ` : `
                        <div class="quantity-selector">
                            <label for="quantity">Количество:</label>
                            <div class="quantity-input-group">
                                <button class="quantity-btn minus"><i class="fas fa-minus"></i></button>
                                <input type="number" id="quantity" min="1" max="50" value="1" class="quantity-input">
                                <button class="quantity-btn plus"><i class="fas fa-plus"></i></button>
                            </div>
                            <p class="quantity-price">Итого: <span id="totalPrice">${product.price}</span>₽</p>
                        </div>
                    `}
                    
                    <button class="btn btn-block" id="addToCartBtn">
                        <i class="fas fa-cart-plus"></i> Добавить в корзину
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Добавляем обработчики событий
    if (product.type === 'weight') {
        const weightInput = document.getElementById('weight');
        const minusBtn = document.querySelector('.weight-btn.minus');
        const plusBtn = document.querySelector('.weight-btn.plus');
        const totalPrice = document.getElementById('totalPrice');
        
        minusBtn.addEventListener('click', () => {
            let value = parseFloat(weightInput.value);
            if (value > 0.1) {
                weightInput.value = (value - 0.1).toFixed(1);
                updateTotalPrice();
            }
        });
        
        plusBtn.addEventListener('click', () => {
            let value = parseFloat(weightInput.value);
            if (value < 10) {
                weightInput.value = (value + 0.1).toFixed(1);
                updateTotalPrice();
            }
        });
        
        weightInput.addEventListener('input', updateTotalPrice);
        
        function updateTotalPrice() {
            const weight = parseFloat(weightInput.value);
            const total = (product.price * weight).toFixed(2);
            totalPrice.textContent = total;
        }
    } else {
        const quantityInput = document.getElementById('quantity');
        const minusBtn = document.querySelector('.quantity-btn.minus');
        const plusBtn = document.querySelector('.quantity-btn.plus');
        const totalPrice = document.getElementById('totalPrice');
        
        minusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
                updateTotalPrice();
            }
        });
        
        plusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value < 50) {
                quantityInput.value = value + 1;
                updateTotalPrice();
            }
        });
        
        quantityInput.addEventListener('input', updateTotalPrice);
        
        function updateTotalPrice() {
            const quantity = parseInt(quantityInput.value);
            const total = (product.price * quantity).toFixed(2);
            totalPrice.textContent = total;
        }
    }
    
    // Обработчик для кнопки добавления в корзину
    document.getElementById('addToCartBtn').addEventListener('click', () => {
        if (product.type === 'weight') {
            const weight = parseFloat(document.getElementById('weight').value);
            addToCart(product, 1, weight);
        } else {
            const quantity = parseInt(document.getElementById('quantity').value);
            addToCart(product, quantity);
        }
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    displayProduct();
});