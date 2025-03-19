import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Get Alembic config and set up logging if file exists
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import DB URL and metadata
from app.databases.main_db import DATABASE_URL, Base

# Metadata for migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Configure context for offline migrations
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        # Run offline migrations
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    # Configure context with active connection
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        # Run online migrations
        context.run_migrations()


async def run_async_migrations() -> None:
    # Prepare async engine configuration
    connect_config = config.get_section(config.config_ini_section, {})
    connect_config["sqlalchemy.url"] = DATABASE_URL

    # Create async engine without pooling
    connectable = async_engine_from_config(
        connect_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Run migrations with connection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    # Run async migrations using asyncio
    asyncio.run(run_async_migrations())


# Ensure online mode
assert not context.is_offline_mode()

run_migrations_online()
