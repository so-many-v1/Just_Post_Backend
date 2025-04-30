## JustPost Backend

## Основное серверное приложение, реализующее логику пользователей, регистрацию, аутентификацию, создание постов, подписку на пользователей и взаимодействием с сервисом нотификации с использованием Kafka.

# 🚀 Реализовано

# 📩 Регистрация с подтверждением email через ссылку

# 🔐 Аутентификация по логину и паролю

# 📝 Создание и удаление постов

# 🤝 Подписка на пользователей 

# 🔔 Интеграция с Kafka (producer) для отправки событий:

- register_event

- login_event

- create_post_event

- delete_user_event

⚙️ Поддержка асинхронной работы через FastAPI, SQLAlchemy (async), alembic

## 🧱 Стек технологий
Python 3.12

FastAPI

PostgreSQL 15

Kafka 

Alembic (миграции)

Docker + Docker Compose

## Запуск

В корне проекта создай .env файл, например:

.env
DB_USER=postgres
DB_PASS=password
DB_HOST=localhost
DB_PORT=5430
DB_NAME=just_post_db

## Подними базу данных, Kafka и backend:

docker compose up --build

⚠️ Важно

Kafka может стартовать дольше других сервисов. Убедись, что она действительно работает, прежде чем запускать продюсера или консюмера. Можно подождать в логах:

## Запуск приложения из корня проекта

 cd backend/

 pip install -r requirements.txt

 uvicorn main:app --reload
