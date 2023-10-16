Avtoria parser
===

Test task from dataox

## DIRECTORY STRUCTURE
```
|—— .env_example
|—— alembic.ini
|—— docker-compose.yml
|—— Dockerfile
|—— requirements.txt
|—— src
|    |—— config
|        |—— __init__.py
|    |—— core
|        |—— app.py
|        |—— parser.py
|        |—— settings.py              your settings for whole app   
|        |—— user_agent.py
|        |—— __init__.py
|    |—— database
|        |—— core                     here is your connection or main class
|            |—— connection.py
|            |—— database.py
|            |—— mediator.py
|            |—— unit_of_work.py
|            |—— __init__.py
|        |—— dumps
|        |—— exceptions.py
|        |—— interfaces                your interfaces for database
|            |—— repositories
|                |—— crud.py
|                |—— __init__.py
|            |—— __init__.py
|        |—— migrations                your db stages and versions
|            |—— env.py
|            |—— README
|            |—— script.py.mako
|            |—— versions
|                |—— 5d041aef7cbf_.py
|                |—— __init__.py
|            |—— __init__.py
|        |—— models                    your db models
|            |—— base.py
|            |—— phone.py
|            |—— ticket.py
|            |—— __init__.py
|        |—— repositories              your repo for work with db models and queries
|            |—— base.py
|            |—— crud.py
|            |—— phone.py
|            |—— ticket.py
|            |—— __init__.py
|        |—— __init__.py
|    |—— dto                           here is yours data structures for database
|        |—— autoria.py
|        |—— converters.py
|        |—— phone.py
|        |—— ticket.py
|        |—— __init__.py
|    |—— session
|        |—— aiohttp.py
|        |—— base.py
|        |—— errors.py
|        |—— response.py
|        |—— __init__.py
|    |—— __main__.py

```

## download
```
git clone https://github.com/KhizhnyakSergey/avtoria_parser
```
# Installation
```
pip install -r requirements.txt
```
Create db and tables. 
```
alembic revision --autogenerate -m 'initial' && alembic upgrade head
```

Start app:

for Windows:
```
python -m src
```
for Unix:
```
python3 -m src
```
And thats it!
# Docker
## Unix:
```
make docker_build
```
Add migrations:
```
docker-compose run --rm migrate
```
```
make docker_up
```
## Windows:
```
docker-compose build && docker-compose run --rm migrate && docker-compose up -d
```
## ENV_FILE
First of all rename your `.env_example` to `.env`
