# Organization-Search API (FastAPI, SQLAlchemy)

## Запуск
- Создайте файл `.env` (в корне)
- Запустите сервисы (бекенд автоматически выполнит миграции и наполнит БД тестовыми данными при первом старте):
  ```bash
  docker compose up --build
  ```

## Работа с API
- Документация: `http://localhost:5000/api/docs`.
- Получение токена: `POST /api/v1/auth/token` (без тела). Ответ содержит `accessToken`.
- Добавьте заголовок `Access-Token: <accessToken>` для всех запросов к защищённым эндпоинтам `/api/v1/...`.
