# tg_bot_geolocation

```bash
apt install python3.10-venv
```
```bash
source venv/bin/activate
```
Upgrade package installer for Python and install packages:
```bash
pip install --upgrade pip
```
https://www.psycopg.org/docs/install.html
```bash
pip install psycopg2-binary
```
pip install python-dotenv
pip install python-telegram-bot --upgrade
pip install "python-telegram-bot[all]"

Start with args
```bash
python main.py
```

```bash
deactivate
```


Для подключения к базе данных PostgreSQL вы должны знать следующие параметры:
host
Это имя сервера или IP-адрес, на котором работает сервер PostgreSQL. 
Если вы работаете на локальной машине, вы можете использовать localhost или его IP-адрес, то есть 127.0.0.1. 
Если ваш сервер PostgreSQL размещен на удаленном сервере, вам потребуется ввести соответствующий IP-адрес или доменное имя pynative.com.
database
Это имя базы данных, к которой вы хотите подключиться. 
Вы должны создать эту базу данных на вашем сервере PostgreSQL перед подключением к ней postgresqltutorial.com.
user и password
Это имя пользователя и пароль, которые вы используете для работы с PostgreSQL. 
По умолчанию имя пользовате��я для базы данных PostgreSQL - postgres. 
Пароль задается пользователем во время установки PostgreSQL pynative.com.
```python
connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)
```
