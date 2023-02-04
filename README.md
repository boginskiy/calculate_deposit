# Калькулятор банковских вкладов

### **Описание**
API-сервис позволяет помесячно рассчитать вклад в банке нарастающим эффектом.

Принимает параметры:
* date - дата заявки, формат "31.12.2023"
* periods - количество месяцев по вкладу, от 1 до 60 мес.
* amount - первоначальная сумма вклада, от 10.000 до 3.000.000 руб.
* rate - процент по вкладу, от 1 до 8 %

### **Технологии**
* python 3.8
* fastapi 0.89.1
* starlette 0.22.0
* pydantic 1.10.4
* python-dateutil 2.8.2
* uvicorn 0.20.0

### **Быстрый запуск проекта через образ на DockerHub**
* _Перед запуском у вас должен быть установлен [Docker](https://docs.docker.com/engine/install/ubuntu/)_

Клонировать образ проекта с DockerHub
```
sudo docker pull boginskiy/lighthousebot:v1.1
```

Запустить контейнер с образом
```
sudo docker run boginskiy/lighthousebot:v1.1
```

### **Запуск проекта через Dockerfile**
Клонировать проект c GitHub
```
git clone git@github.com:boginskiy/LightHouseBot.git
```

Задать свои переменные окружения. Подробности в _"Шаблон наполнения env-файла"_
```
ENV BOT_TOKEN '5879466790:AAFAfXYX84VM4x-ze2LrSWiMXB9Oi84ELPQ'
ENV ID_ADMIN 5339343954
```

Собрать образ проекта. Команда выполняется с корневой директории.
```
sudo docker build -t <имя_проекта> .
```

Запустить контейнер с образом
```
sudo docker run <имя_проекта>
```

### **Шаблон наполнения env-файла**
Ознакомьтесь с **.env.example** файлом. На его основе со своими данными создайте **.env** файл в директории проекта.

```
.env.example

BOT_TOKEN = 'API токен чат бота'
ID_ADMIN = 'ID чата для администрирования. Например ID чата хозяина бота'
```

У вас должно получиться так:
```
.env

BOT_TOKEN = '5879439590:AAFAfXYX84VM4x-ze2LrSWiMXB9Oi84ELPQ'
ID_ADMIN = 5339829954
```

### **Запуск проекта в dev режиме на Linux**
Клонировать проект c GitHub
```
git clone git@github.com:boginskiy/LightHouseBot.git
```
Установить виртуальное окружение venv
```
python3 -m venv venv
```
Активировать виртуальное окружение venv
```
source venv/bin/activate
```
Обновить менеджер пакетов pip
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
Запуск
```
python3 lighthouse.py
```

### **Примеры запросов API**
#### **Запросы к AUTH (Регистрация пользователей и выдача токенов):**
Регистрация нового пользователя. (POST): `http://127.0.0.1:8000/api/v1/auth/signup/`

```
    {
        "email": "string",
        "username": "string"
    }
```

* _Использовать имя 'me' в качестве username запрещено_
* _Доступно любому пользователю_
---

###### Запрос к AUTH
Получение JWT-токена. (POST): `http://127.0.0.1:8000/api/v1/auth/token/`

```
    {
        "username": "string"
        "confirmation_code": "string"
    }
```
* _confirmation_code - при регистрации нового пользователя в директории проекта **api_yamdb/sent_emails** появляется файл.log в котором находится данный код_
* _Доступно любому пользователю_
---

### **Автор**
[Богинский Дмитрий](https://github.com/boginskiy) - python разработчик