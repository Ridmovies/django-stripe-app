# Указываем базовый образ, который будет использоваться для сборки контейнера.
FROM python:3.10-slim-bullseye

# Устанавливаем необходимые зависимости для работы с Docker.
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev git curl

# Создаем рабочую директорию внутри контейнера.
WORKDIR /app

# Копируем файл requirements.txt в контейнер.
COPY ./requirements.txt .

# Устанавливаем пакеты из файла requirements.txt.
RUN pip install -r requirements.txt

# Копируем весь код проекта в контейнер.
COPY . .

# Экспортируем порт 8000, чтобы приложение было доступно снаружи контейнера.
EXPOSE 8000

# # Запускаем команду для выполнения миграции базы данных перед запуском сервера.
# CMD ["python", "manage.py", "migrate"]
#
# # Команда для запуска веб-сервера Django.
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Используем ENTRYPOINT для выполнения двух команд последовательно.
ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]