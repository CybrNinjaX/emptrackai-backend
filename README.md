# EmpTrackAI Backend

Django backend for admin registration using PostgreSQL.

## Requirements

* Python 3.14+
* PostgreSQL
* PostgreSQL database: `emptrackai`
* PostgreSQL user: `emptrackai`

---

## Setup

### macOS / Linux

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

### Windows

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
pip install django "psycopg[binary]" python-dotenv
```

```bash
which python
python --version
python -m pip --version
```
```bash
python -m pip install --upgrade pip

python -m pip install django psycopg[binary] python-dotenv
```

---

## PostgreSQL Setup

Make sure PostgreSQL is installed and running.

### Open PostgreSQL on macOS / Linux

```bash
psql postgres
```



Create the PostgreSQL user:

```sql
CREATE USER emptrackai WITH PASSWORD 'your_password';
```

Create the database:

```sql
CREATE DATABASE emptrackai
    OWNER emptrackai;
```

Grant privileges:

```sql
GRANT ALL PRIVILEGES ON DATABASE emptrackai TO emptrackai;
```

Check the PostgreSQL users:

```sql
\du
```

Check the databases:

```sql
\l
```

Exit PostgreSQL:

```sql
\q
```

> Replace `your_password` with your actual PostgreSQL password.

---

## Environment Variables

Create the local environment file:

### macOS / Linux

```bash
cp .env.example .env
```

### Windows

```powershell
copy .env.example .env
```

Update `.env` with your PostgreSQL credentials:

```env
DB_NAME=emptrackai
DB_USER=emptrackai
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file is ignored by Git and must not be committed.

---

## Database Connection

Test the PostgreSQL connection:

```bash
psql -h localhost -U emptrackai -d emptrackai
```

Enter your PostgreSQL password when prompted.

Exit:

```sql
\q
```

---

## Migrations

Apply Django migrations:

```bash
python manage.py migrate
```

If the `admins` table already exists and matches the Django model, use:

```bash
python manage.py migrate --fake-initial
```

Check the Django project:

```bash
python manage.py check
```

---

## Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

The server runs at:

```text
http://127.0.0.1:8000/
```

---

## API

### Admin Registration

Example request:

```http
POST /api/register/
Content-Type: application/json
```

Example JSON:

```json
{
  "username": "api_test",
  "company_name": "Acme Corp",
  "email": "api_test@example.com",
  "password": "your_password",
  "confirm_password": "your_password"
}
```

Passwords are stored using Django password hashing.

Login and JWT session APIs are not included yet.

---

## Project Structure

```text
emptrackai-backend/
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── employees/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── .env
├── .env.example
├── register.json
└── README.md
```

---

## Important

Do not commit `.env` to Git.

Make sure `.gitignore` contains:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

Never upload real database passwords, API keys, or other secrets to GitHub.
