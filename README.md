Yandex Forms Clone API

Данный проект представляет собой упрощенную реализацию бэкенда сервиса Яндекс Формы. Приложение разработано на FastAPI с использованием SQLAlchemy и PostgreSQL.
🛠 Технологический стек

    Backend: FastAPI, Python 3.13+

    Database: PostgreSQL

    ORM: SQLAlchemy 2.0

    Validation: Pydantic v2

    Auth: JWT (JSON Web Tokens), bcrypt

    Infrastructure: Docker, Docker Compose

🚀 Как запустить проект
Вариант 1: Docker (Рекомендуемый)

Этот способ автоматически поднимет базу данных и запустит приложение.

    Убедитесь, что у вас установлен Docker Desktop.

    В корне проекта создайте файл .env на основе примера ниже.

    Запустите контейнеры:
    code Bash

    docker-compose up --build

    API будет доступно по адресу: http://localhost:8000

    Интерактивная документация: http://localhost:8000/docs

Вариант 2: Локальный запуск

    Создайте виртуальное окружение: python -m venv venv

    Активируйте его: source venv/bin/activate

    Установите зависимости: pip install -r requirements.txt

    Поднимите PostgreSQL (локально или через docker-compose).

    Создайте файл .env и укажите там данные для подключения к БД.

    Запустите сервер: uvicorn app.main:app --reload

⚙️ Настройка окружения (.env)

Создайте файл .env в корне проекта:
code Env

DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/yandex_forms
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=45

🧩 Функционал API

    Auth: Регистрация, авторизация, получение данных текущего пользователя.

    Forms: Создание, чтение, редактирование и удаление форм. Поддержка текстовых полей, radio-кнопок и чекбоксов.

    Responses: Отправка ответов на формы и просмотр результатов владельцем формы.

    Filters: Поиск по заголовку формы и сортировка списка форм.

🧪 Тестирование

Для тестирования API вы можете использовать Swagger UI (/docs) или импортировать файл postman_collection.json в Postman.