# Organization-Search API (FastAPI, SQLAlchemy)

## Запуск
- Создайте файл `.env` (в корне)
- Соберите контейнер и подготовьте зависимости:
  ```bash
  docker compose build backend
  ```
- Примените миграции:
  ```bash
  docker compose run --rm backend alembic upgrade head
  ```
- Запустите сервисы (бекенд и базу):
  ```bash
  docker compose up backend
  ```

## Работа с API
- Документация: `http://localhost:5000/api/docs`.
- Получение токена: `POST /api/v1/auth/token` (без тела). Ответ содержит `accessToken`.
- Добавьте заголовок `Access-Token: <accessToken>` для всех запросов к защищённым эндпоинтам `/api/v1/...`.
