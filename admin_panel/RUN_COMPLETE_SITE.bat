@echo off
REM Запуск сервера Рыбный День
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎣 Рыбный День - Запуск сервера                     ║
echo ║   Loading Fish Day Server...                           ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Переходим в папку проекта
cd /d "%~dp0admin_panel"

echo [✓] Переход в директорию: %CD%
echo.

REM Проверяем что Python установлен
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [✗] ОШИБКА: Python не найден!
    echo.
    echo Установите Python с https://www.python.org/downloads/
    echo И убедитесь что python добавлен в PATH
    echo.
    pause
    exit /b 1
)

REM Проверяем что manage.py существует
if not exist "manage.py" (
    echo [✗] ОШИБКА: manage.py не найден!
    echo.
    echo Убедитесь что вы находитесь в папке admin_panel
    echo.
    pause
    exit /b 1
)

REM Проверяем что виртуальное окружение активно (если нужно)
if not exist "venv" (
    echo [!] Виртуальное окружение не найдено
    echo     Рекомендуется использовать: python -m venv venv
    echo.
)

REM Запускаем сервер
echo [•] Запуск Django сервера...
echo [•] Сервер будет доступен по адресу: http://localhost:8000
echo.
echo Для остановки сервера нажмите Ctrl+C
echo ================================================================
echo.

python manage.py runserver

REM Если сервер упал - показываем ошибку
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [✗] Ошибка при запуске сервера!
    echo.
    echo Возможные решения:
    echo 1. Убедитесь что порт 8000 не занят
    echo    Запустите на другом порту: python manage.py runserver 8001
    echo.
    echo 2. Проверьте зависимости:
    echo    pip install -r requirements.txt
    echo.
    echo 3. Проверьте БД:
    echo    python manage.py migrate
    echo.
    pause
)
