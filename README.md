# Система выбора стратегий реагирования на инциденты

Django-приложение разработано в рамках выполнения выпускной работы на тему "Автоматизированная система выбора стратегий реагирования на IT-инциденты". В системе хранятся данные о добавленных экспертами инцидентах (описание, возможные причины, возможные стратегии решения, критерии оценки стратегий). Также реализован процесс выбора наиболее подходящей стратегии решения инцидента с применением методов теории принятия решений, исходя из оценок эффективности стратегий экспертом/экспертами в зависимости от возможных причин.

Стек: Python, Django, PostgreSQL, Docker, Yandex.Tank, jQuery, HTML, CSS.

## Зависимости

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Использование веб-приложения локально

1. Клонирование репозитория:

   ```bash
   git clone https://github.com/pdogger/vkr_incidents.git
   cd vkr_incidents

2. Запуск Django-приложения:

   ```bash
   docker-compose up -d --build

3. Веб-приложение доступно по адресу `http://localhost/`

4. Панель администратора доступна по адресу `http://localhost/admin`.
Данные для входа задаются в файле `.env`: `DJANGO_SUPERUSER_USERNAME` и `DJANGO_SUPERUSER_PASSWORD`.

5. Завершение работы:

   ```bash
   docker-compose down