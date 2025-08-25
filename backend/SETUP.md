# Setting Up the Backend

Welcome this file will give guidance on how to set up the backend and run it.

## Create virtual Environment

```sh
python3 -m venv venv
```

## Activate virtual environment

```sh
source venv/bin/activate
```

## Installing uv package

```sh
pipx install uv
```

## Initializing project

```sh
uv init
```

## Installing and permanently adding a dependency to your project

```sh
uv add <package>
```

### To update the uv.lock file with the dependencies

```sh
uv sync
```

### Running file

```sh
uv run main.py
```
