# Backend

This guide explains:

- How to initialize and manage database migrations using Alembic.
- How to run the backend.

## Alembic Initialization

Create the Alembic directory structure :

```sh
alembic init -t async alembic
```

## Managing Migrations

### 1. Generate a Migration

- For the initial migration:
  ```sh
  alembic revision --autogenerate -m "initial migration"
  ```
- For further migration:
  ```sh
  alembic revision --autogenerate -m "Add field"
  ```

### 2. Apply Migrations

Update the database :

```sh
alembic upgrade head
```

## Running the Backend

To start the backend in dev mode, use the following command:

```sh
uvicorn app.main:app --reload
```

> This will launch the application with automatic reloading enabled.
