# Foodgram
### Описание
Проект **Foodgram** позволяет делиться рецептами и скачивать списки продуктов

### Установка
Проект собран в Docker 20.10.06 и содержит четыре образа:
- backend - образ бэка проекта
- frontend - образ фронта проекта
- postgres - образ базы данных PostgreSQL v 12.04
- nginx - образ web сервера nginx
#### Команда клонирования репозитория:
```bash
git clone https://github.com/Krono05/foodgram-project-react 
```
#### Запуск проекта:
- [Установите Докер](https://docs.docker.com/engine/install/)
- Выполнить команду: 
```bash
docker pull tamir88/foodgram-project-react :latest
```
#### Первоначальная настройка Django:
```bash
- docker-compose exec web python manage.py migrate --noinput
- docker-compose exec web python manage.py createsuperuser
- docker-compose exec web python manage.py collectstatic --no-input
```
#### Заполнение .env:
Чтобы добавить переменную в .env необходимо открыть файл .env в корневой директории проекта и поместить туда переменную в формате имя_переменной=значение.
Пример .env файла:

DB_ENGINE=my_db
DB_NAME=db_name
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db_host
DB_PORT=db_port

#### Адрес сервера:
http://62.84.113.248/

#### Для панели администратора:

admin: super@pangur-ban.ru

password: 123456789qwerty

