# telegram_bot_geolocation_python

[Rust version](https://github.com/antonovmike/telegram_bot_geolocation_rust) of this telegram bot

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
Install psycopg2-binary https://www.psycopg.org/docs/install.html
```bash
pip install psycopg2-binary
```
pip install python-dotenv

Start with args
```bash
python main.py
```

```bash
deactivate
```

Postgres
```bash
sudo su postgres
psql
CREATE USER tg_bot WITH password 'qwerty';
CREATE DATABASE telegram_db OWNER tg_bot;
\connect telegram_db;
```
