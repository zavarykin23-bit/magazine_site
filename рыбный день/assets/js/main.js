// DOM элементы
const cartCount = document.getElementById('cartCount');
const cartFloatCount = document.getElementById('cartFloatCount');
const scrollTop = document.getElementById('scrollTop');

// Данные корзины
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Обновление счетчика корзины
function updateCartCount() {
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    if (cartCount) {
        cartCount.textContent = totalItems;
    }
    if (cartFloatCount) {
        cartFloatCount.textContent = totalItems;
    }
}

// Кнопка прокрутки наверх (только если элемент существует)
if (scrollTop) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTop.style.display = 'flex';
        } else {
            scrollTop.style.display = 'none';
        }
    });

    scrollTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    
    // Анимация появления элементов при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.product-card, .step, .feature').forEach(el => {
        observer.observe(el);
    });
});