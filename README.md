# ССК Альянс

Web app for managing a student sports club league. Built with Flask, Flask-Admin, and SQLAlchemy.

## Русский

Веб-приложение для управления студенческим спортивным клубом. Используются Flask, Flask-Admin и SQLAlchemy.

### Возможности

- Таблица лиги по командам
- Команды, матчи и топ игроков по виду спорта
- Админ-панель для управления контентом
- JSON API для данных по спорту

### Быстрый старт (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python create_db.py
python run.py
```

### Быстрый старт (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python create_db.py
python run.py
```

Откройте http://127.0.0.1:5000 в браузере.

### Админ-пользователь

```bash
python create_admin.py
```

Учетные данные по умолчанию (из `create_admin.py`):

- Логин: admin
- Пароль: admin123

### Конфигурация

Задайте надежный `SECRET_KEY` через переменные окружения. Пример (PowerShell):

```powershell
$env:SECRET_KEY = "change-me"
```

В `app/__init__.py` можно читать его через `os.getenv("SECRET_KEY")`.

### Деплой

- Используйте production WSGI сервер (например, Gunicorn на Linux).
- Отключите `debug=True` в проде.
- Настройте `SQLALCHEMY_DATABASE_URI` через переменные окружения.

## Features

- League table by team
- Teams, matches, and top players per sport
- Admin panel for content management
- JSON API for sport data

## Requirements

- Python 3.12+

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Initialize the database.
4. Run the app.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python create_db.py
python run.py
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python create_db.py
python run.py
```

Open http://127.0.0.1:5000 in your browser.

## Admin user

Create an admin user:

```bash
python create_admin.py
```

Default credentials (from `create_admin.py`):

- Username: admin
- Password: admin123

## API

Get data for a tournament:

```
GET /api/tournament/<tournament_id>
```

Response:

```json
{
  "tournament": {
    "id": 1,
    "name": "Alliance League",
    "season": "2026",
    "status": "active",
    "sport": "Football"
  },
  "standings": [
    {
      "name": "Team A",
      "logo": null,
      "wins": 3,
      "draws": 1,
      "losses": 0,
      "points": 10,
      "goal_difference": 6
    }
  ],
  "teams": [
    {
      "name": "Team A",
      "sport": "Football",
      "logo": null
    }
  ],
  "matches": [
    {
      "team1": "Team A",
      "team2": "Team B",
      "score1": 2,
      "score2": 1,
      "date": "2026-05-10"
    }
  ],
  "players": [
    {
      "name": "Player 1",
      "goals": 5,
      "team": "Team A"
    }
  ]
}
```

## Notes

- SQLite database file: `site.db`
- Configure the database URL in `app/__init__.py`.

## Configuration

Set a strong secret key for production. Example (PowerShell):

```powershell
$env:SECRET_KEY = "change-me"
```

You can read it in `app/__init__.py` using `os.getenv("SECRET_KEY")`.

## Deployment

- Use a production WSGI server (for example, Gunicorn on Linux).
- Disable `debug=True` in production.
- Configure `SQLALCHEMY_DATABASE_URI` via environment variables.
