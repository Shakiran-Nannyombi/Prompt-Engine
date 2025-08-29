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

## Running Tests with pytest

Run this pytest command in the /tests folder

```sh
python -m pytest filename.py -v
```

Running streamlite demo

```sh
streamlit run streamlite_app.py
```
