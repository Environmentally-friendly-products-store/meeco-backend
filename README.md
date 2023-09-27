# ecome-backend
Интернет-магазин экологически чистых товаров без отходов. Товары для уборки, домашнего хозяйства, красоты и личной гигиены, изготовленные из безопасных и чистых ингредиентов и др. Это больше, чем тренд и просто модное направление, это может быть этическое, экологически сознательное решение.

![EcoMe-backend](https://github.com/Environmentally-friendly-products-store/meeco-backend/actions/workflows/backendmain.yml/badge.svg?event=push)

# Стек технологий

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Локальное развертывание проекта
Клонировать репозиторий
`git clone git@github.com:Environmentally-friendly-products-store/meeco-backend.git`
В папке backend cоздать виртуальное окружение, обновить установщик пакетов pip, установить зависимости:
```
cd backend
py 3.11 -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
pip install requirements.txt
```
Установить в файле meeco/settings.py Debug=True.

Применить миграции, создать суперпользователя, запустить сервер:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Панель администратора localhost:8000/admin/

Доступные endpoints в API:
#### Регистрация пользователя
POST  /api/v1/register/
#### Пользователи
GET /api/v1/users/me/
#### Аутентификация пользователя JWT
POST /api/v1/token/

POST /api/v1/token/refresh/

POST /api/v1/token/verify/
#### Категории
GET /api/v1/categories/

POST /api/v1/categories/

GET /api/v1/categories/{id}/

PATCH /api/v1/categories/{id}/
#### Акции
GET /api/v1/events/

POST /api/v1/events/

GET /api/v1/events/{id}/

PATCH /api/v1/events/{id}/
#### Товары 
GET /api/v1/products/

POST /api/v1/products/

GET /api/v1/products/{id}/

PATCH /api/v1/products/{id}/

DELETE /api/v1/products/{id}/
#### Корзина
POST /api/v1/products/{id}/shopping_cart/

PATCH /api/v1/products/{id}/shopping_cart/

DELETE /api/v1/products/{id}/shopping_cart/
#### Заказы
GET /api/v1/orders/

POST /api/v1/orders/

GET /api/v1/orders/{id}/

PATCH /api/v1/orders/{id}/

DELETE /api/v1/orders/{id}/

Более подробную информацию см. в файле ../docs/ApiDoc.yaml
