# Setting Up the Backend

Welcome this file will give guidance on how to set up the backend and run it.

## Create virtual Environment

```sh
python3 -m venv venv
```

### Activate virtual environment

```sh
source venv/bin/activate
```

## Installing uv package

```sh
pipx install uv
```

### Initializing project

```sh
uv init
```

### Installing and permanently adding a dependency to your project

```sh
uv add <package>
```

### To update the uv.lock file with the dependencies

```sh
uv sync
```

### Running file

```sh
uv run app/api/main.py
```

## setting up postgress-sql database

### Install postgress sql

```sh
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

### Enabling and starting postgresql

```sh
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Check status

```sh
sudo systemctl status postgresql
```

### Switch to postgress default superuser and shell

```sh
sudo -i -u postgres
psql
```

### creating database

```sh
CREAET DATABASE promptengine_db;
CREATE USER languser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE promptengine_db TO languser;
```

### Exit shell and test connection

```sh
\q
psql -h localhost -U languser -d promptengine_db
```

## Migration to Supabase

Supabase provides a hosted PostgreSQL database. To migrate:

1.  **Get Credentials**: Go to your Supabase Project Settings > Database and copy the **Connection string** (choose Python/psycopg).
2.  **Update .env**: Paste the connection string into `DATABASE_URL`.
3.  **Initialize Database**: Run the schema script to create application tables.

```sh
uv run python -c "from database import init_db; init_db()"
```

4.  **Seed Data**: Populate initial frameworks and data.

```sh
uv run python seed.py
```

## Running Tests with pytest

Run this pytest command in the /tests folder

```sh
python -m pytest filename.py -v
```

Running streamlite demo

```sh
streamlit run streamlite_app.py
```
