// Данные товаров
const products = [
    {
        id: 1,
        name: 'Вобла вяленая',
        price: 780,
        type: 'weight',
        image: 'assets/images/voBlya.png',
        description: 'Вяленая вобла весеннего улова. Средний размер рыбки 22-25 см',
        category: 'fish'
    },
    {
        id: 2,
        name: 'Чехонь вяленая',
        price: 460,
        type: 'weight',
        image: 'assets/images/chehoni.png',
        description: 'Вяленая чехонь славится своим жиром. При разделки все руки в нем!',
        category: 'fish'
    },
    {
        id: 3,
        name: 'Камбала-ерш вяленая',
        price: 460,
        type: 'weight',
        image: 'assets/images/cambala.png',
        description: 'Камбала-ерш - вкусная рыба, богатая полезными веществами.',
        category: 'fish'
    },
    {
        id: 4,
        name: 'Щука потрошенная вяленая',
        price: 880,
        type: 'weight',
        image: 'assets/images/chuka.png',
        description: 'Щука - изысканная деликатесная рыба с неповторимым ароматом.',
        category: 'fish'
    },
    {
        id: 5,
        name: 'Карп потрошенный вяленый',
        price: 650,
        type: 'weight',
        image: 'assets/images/carp.png',
        description: 'Карп рыба с нежным мясом и сладковатым ароматным вкусом.',
        category: 'fish'
    },
    {
        id: 6,
        name: 'Густера вяленая',
        price: 310,
        type: 'weight',
        image: 'assets/images/taran.png',
        description: 'Густера является традиционно русской закуской к пенному.',
        category: 'fish'
    },
    {
        id: 7,
        name: 'Сыр "ДЖИЛ" копченый',
        price: 105,
        type: 'piece',
        weight: 50,
        image: 'assets/images/капчени.png',
        description: 'Сыр "ДЖИЛ" копченый - вкусный, натуральный, высокого качества.',
        category: 'snack'
    },
    {
        id: 8,
        name: 'Сыр "ДЖИЛ" балык-белый',
        price: 110,
        type: 'piece',
        weight: 50,
        image: 'assets/images/молочный.png',
        description: 'Сыр "ДЖИЛ" молочный с особым ароматом и нежной текстурой.',
        category: 'snack'
    },
    {
        id: 9,
        name: 'Сыр "ДЖИЛ" балык-копченый',
        price: 110,
        type: 'piece',
        weight: 50,
        image: 'assets/images/другой капчении.png',
        description: 'Сыр "ДЖИЛ" балык-копченый из натурального сырного сычужного фермента.',
        category: 'snack'
    },
    {
        id: 10,
        name: 'Мясо кальмара со вкусом краба',
        price: 650,
        type: 'weight',
        weight: 500,
        image: 'assets/images/кальмар.png',
        description: 'Мясо кальмара имеет уникальный вкус, объединяющий свежесть морской пищи и аромат краба.',
        category: 'snack'
    },
    {
        id: 11,
        name: 'Соломка из Судака',
        price: 510,
        type: 'weight',
        weight: 500,
        image: 'assets/images/судак.png',
        description: 'Соломка "Судак" производится путем высушивания свежей рыбы.',
        category: 'snack'
    },
    {
        id: 12,
        name: 'Соломка из Горбуши',
        price: 550,
        type: 'weight',
        weight: 500,
        image: 'assets/images/горбуша.png',
        description: 'Соломка из горбуши - деликатесное рыбное блюдо с неповторимым вкусом.',
        category: 'snack'
    }
];

// Функция для отображения товаров
function displayProducts(category) {
    const productsGrid = category === 'fish' 
        ? document.querySelector('.products-grid')
        : document.querySelector('.snacks-grid');
    
    if (!productsGrid) return;
    
    const filteredProducts = products.filter(product => product.category === category);
    
    productsGrid.innerHTML = filteredProducts.map(product => `
        <div class="product-card" data-id="${product.id}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-price">${product.price}₽ ${product.type === 'weight' ? '/ кг' : '/ шт'}</p>
                <p class="product-description">${product.description}</p>
                <a href="product.html?id=${product.id}" class="btn btn-block">Выбрать вес/количество</a>
            </div>
        </div>
    `).join('');
}

// Инициализация товаров при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    displayProducts('fish');
    displayProducts('snack');
});