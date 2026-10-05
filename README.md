# EmpTrackAI Backend

Django backend for admin registration using PostgreSQL.

## Requirements

- Python 3.14+
- PostgreSQL
- A PostgreSQL database and user named `emptrackai`

## Setup

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate

```
windows
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```



Install dependencies:

```bash
pip install django "psycopg[binary]" python-dotenv
```

Create the local environment file:

```bash
cp .env.example .env
```

Update `.env` with the PostgreSQL credentials:

```env
DB_NAME=your_DB_Name
DB_USER=your_DB_User
DB_PASSWORD=your_Password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file is ignored by Git and must not be committed.


## Migrations

Apply Django migrations:

```bash
./venv/bin/python manage.py migrate
```

If the `admins` table already exists and matches the Django model, use:

```bash
./venv/bin/python manage.py migrate --fake-initial
```

Check the project:

```bash
./venv/bin/python manage.py check
```

## Run the Server

```bash
./venv/bin/python manage.py runserver
```

The server runs at `http://127.0.0.1:8000/`.

Passwords are stored as Django password hashes. Login and JWT session APIs are not included yet.

## Project Structure

```text
config/
  settings.py
  urls.py
employees/
  migrations/
  models.py
  urls.py
  views.py
manage.py
.env.example
register.json
```
