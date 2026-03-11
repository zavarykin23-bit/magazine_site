// ========== ФУНКЦИЯ ПОИСКА С ПОДДЕРЖКОЙ ОПЕЧАТОК ==========

// Алгоритм Левенштейна для вычисления расстояния между строками
function levenshteinDistance(str1, str2) {
    const len1 = str1.length;
    const len2 = str2.length;
    
    // Матрица для хранения расстояний
    const matrix = Array(len2 + 1).fill(null).map(() => Array(len1 + 1).fill(0));
    
    // Инициализация первой строки и столбца
    for (let i = 0; i <= len1; i++) matrix[0][i] = i;
    for (let j = 0; j <= len2; j++) matrix[j][0] = j;
    
    // Заполнение матрицы
    for (let j = 1; j <= len2; j++) {
        for (let i = 1; i <= len1; i++) {
            const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
            matrix[j][i] = Math.min(
                matrix[j][i - 1] + 1,      // удаление
                matrix[j - 1][i] + 1,      // вставка
                matrix[j - 1][i - 1] + cost // замена
            );
        }
    }
    
    return matrix[len2][len1];
}

// Функция для нечеткого поиска
function fuzzySearch(query, products, maxDistance = 2) {
    if (!query.trim()) return [];
    
    const queryLower = query.toLowerCase().trim();
    const results = [];
    
    products.forEach(product => {
        const nameLower = product.name.toLowerCase();
        const descLower = product.description.toLowerCase();
        
        // Проверка точного совпадения или по началу слова
        if (nameLower.includes(queryLower)) {
            results.push({
                product,
                relevance: 10,
                type: 'exact'
            });
            return;
        }
        
        // Проверка расстояния Левенштейна для названия
        const nameDistance = levenshteinDistance(queryLower, nameLower);
        if (nameDistance <= maxDistance) {
            results.push({
                product,
                relevance: 10 - nameDistance,
                type: 'fuzzy_name'
            });
            return;
        }
        
        // Поиск в словах названия
        const nameWords = nameLower.split(/\s+/);
        for (const word of nameWords) {
            const wordDistance = levenshteinDistance(queryLower, word);
            if (wordDistance <= maxDistance) {
                results.push({
                    product,
                    relevance: (10 - wordDistance) * 0.8,
                    type: 'fuzzy_word'
                });
                return;
            }
            
            // Поиск если query начинается с начала слова
            if (word.startsWith(queryLower)) {
                results.push({
                    product,
                    relevance: (10 - (word.length - queryLower.length)) * 0.9,
                    type: 'partial'
                });
                return;
            }
        }
        
        // Поиск в описании (более низкий приоритет)
        const descWords = descLower.split(/\s+/);
        for (const word of descWords) {
            if (word.includes(queryLower) || levenshteinDistance(queryLower, word) <= 1) {
                results.push({
                    product,
                    relevance: 4,
                    type: 'description'
                });
                return;
            }
        }
    });
    
    // Сортировка по релевантности
    return results
        .sort((a, b) => b.relevance - a.relevance)
        .slice(0, 8) // Максимум 8 результатов
        .map(r => r.product);
}

// Инициализация поиска
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput || !searchResults) return;
    
    let searchTimeout;
    
    // Обработчик ввода
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (!query) {
            searchResults.classList.remove('active');
            searchResults.innerHTML = '';
            return;
        }
        
        // Задержка перед поиском для оптимизации
        searchTimeout = setTimeout(() => {
            const results = fuzzySearch(query, products);
            displaySearchResults(results, searchResults);
        }, 100);
    });
    
    // Закрытие результатов при клике вне поиска
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.remove('active');
        }
    });
    
    // Открытие результатов при фокусе
    searchInput.addEventListener('focus', () => {
        if (searchInput.value.trim() && searchResults.innerHTML) {
            searchResults.classList.add('active');
        }
    });
    
    // Поддержка клавиатуры
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            searchResults.classList.remove('active');
            searchInput.value = '';
        }
    });
}

// Отображение результатов поиска
function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div class="search-no-results">Товары не найдены</div>';
        container.classList.add('active');
        return;
    }
    
    const html = results.map(product => {
        // Исправляем путь к изображению, чтобы оно работало на любой странице
        let imagePath = product.image;
        // Если путь начинается с 'assets/', оставляем как есть (работает везде)
        // Если нет, добавляем префикс для корректной загрузки
        if (!imagePath.startsWith('assets/') && !imagePath.startsWith('./assets/')) {
            imagePath = 'assets/' + imagePath;
        }
        return `
            <div class="search-result-item" onclick="goToProduct(${product.id})">
                <img src="${imagePath}" alt="${product.name}" class="search-result-image">
                <div class="search-result-info">
                    <div class="search-result-name">${product.name}</div>
                    <div class="search-result-price">${product.price}₽</div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
    container.classList.add('active');
}

// Функция для перехода на страницу товара
function goToProduct(productId) {
    window.location.href = `product.html?id=${productId}`;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Проверяем, загружены ли товары
    if (typeof products !== 'undefined') {
        initSearch();
    } else {
        // Если товары еще не загружены, ждем
        const checkProducts = setInterval(() => {
            if (typeof products !== 'undefined') {
                initSearch();
                clearInterval(checkProducts);
            }
        }, 100);
        
        // Таймаут на 5 секунд
        setTimeout(() => clearInterval(checkProducts), 5000);
    }
});
