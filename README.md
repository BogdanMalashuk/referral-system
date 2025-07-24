# 📱 Django Referral System

Простая реферальная система на Django + DRF с авторизацией по SMS-коду(симуляция) и возможностью активировать инвайт-код приглашённого пользователя.

---

## 🚀 Функциональность

- Регистрация по номеру телефона
- Подтверждение через 4-значный код (отправляется в консоль)
- Генерация уникального инвайт-кода при регистрации
- Активация чужого инвайт-кода
- Отображение профиля пользователя, включая:
  - его инвайт-код
  - чей код он активировал
  - список приглашённых пользователей
  - количество приглашённых
- API с документацией через Swagger и ReDoc

---

## 🛠 Используемые технологии

Python 3.12

Django 5.x

Django REST Framework

PostgreSQL

drf-spectacular (Swagger / OpenAPI 3)

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```
git clone https://github.com/BogdanMalashuk/referral-system.git
cd referral-system
```

### 2. Установить зависимости

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Создать .env файл

```
DEBUG=True/False
SECRET_KEY=example_key
ALLOWED_HOSTS=host_1, host_2, ...

DB_NAME=example_name
DB_USER=example_user
DB_PASSWORD=example_password
DB_HOST=example_host
DB_PORT=5432
```

### 4. Применить миграции

```
python manage.py makemigrations
python manage.py migrate
```

### 5. Запустить сервер

```
python manage.py runserver
```
---

## 🔐 Аутентификация

Аутентификация происходит через токен (DRF TokenAuthentication).

Все защищённые эндпоинты требуют заголовок:
```
Authorization: Token <your_token>
```

---

## 🧪 API Документация (Swagger UI)
❗Для получения JSON схемы, ReDoc документации запустите проект локально
и воспользуйтесь ссылками❗

Авторизация в системе: 
![request_code.jpg](project/api/swagger_screenshots/request_code.jpg)

Верификация кода:
![verify_code.jpg](project/api/swagger_screenshots/verify_code.jpg)

Получение профиля
![profile.jpg](project/api/swagger_screenshots/profile.jpg)

Активация инвайт-кода
![activate_code.jpg](project/api/swagger_screenshots/activate_code.jpg)

---

## 🖼️ Шаблоны

Страница авторизации:
![login.jpg](project/web/templates_screenshots/login.jpg)

Верификация кода:
![verifying.jpg](project/web/templates_screenshots/verifying.jpg)

Страница профиля:
![profile.jpg](project/web/templates_screenshots/profile.jpg)

Инвайт-код (активирован)
![activation.jpg](project/web/templates_screenshots/activation.jpg)

Инвайт-код (не активирован)
![activation2.jpg](project/web/templates_screenshots/activation2.jpg)



