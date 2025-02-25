# Django-Stripe Test app

Простое приложение Django с одной html страничкой, который общается со Stripe и создает платёжные формы для товаров.

## Инструменты:
### Основной стек:
- Django
- stripe


### Дополнительные инструменты:
- python-dotenv (Для работы с переменными окружения в Django)



## Roadmap
Основные задачи: 
- [x] Создать item app
- [x] Django Модель Item с полями (name, description, price) 
- [ ] API с двумя методами:
  - [ ] GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
  - [ ] GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
- [ ] Залить решение на Github, описать запуск в Readme.md
- [ ] Опубликовать свое решение чтобы его можно было быстро и легко протестировать. 

Бонусные задачи: 
- [ ] Запуск используя Docker
- [x]  environment variables
- [x] Просмотр Django Моделей в Django Admin панели 
- [ ] Запуск приложения на удаленном сервере, доступном для тестирования
- [ ] Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
- [ ] Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
- [ ] Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
- [ ] Реализовать не Stripe Session, а Stripe Payment Intent.





#### Документация:
http://127.0.0.1:8000/admin/


## DEVELOP
### Django команды:
Запуск приложения
```bash
python manage.py runserver
```

Создать новый проект Django:
```bash
django-admin startproject stripe_test_app
```

Создать новое приложение:
```bash
python manage.py startapp items
```

Создать Супер пользователя
```bash
python manage.py createsuperuser
```

Создать и применить миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Полезные ссылки:
Stripe. Simulate payments to test your integration
https://docs.stripe.com/testing

Stripe. Accept a payment
https://docs.stripe.com/payments/accept-a-payment?integration=checkout