# Hostel Allocation System (Django + PostgreSQL, with PWA shell)

## Quick start (local, SQLite)
1. `python -m venv .venv && . .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (macOS/Linux)
2. `pip install -r requirements.txt`
3. `cp .env.example .env` (or create `.env`)
4. Leave `.env` as-is to use SQLite for quick dev.
5. `python manage.py migrate`
6. Seed demo data: `python manage.py create_demo`
7. `python manage.py runserver`
8. Open http://127.0.0.1:8000

Demo logins:
- Admin: `admin1 / admin123`
- Student: `student1 / student123`

## Switch to PostgreSQL
Set these in `.env`:
