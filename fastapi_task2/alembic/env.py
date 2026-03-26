import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Добавляем путь к проекту - путь к fastapi_task2
current_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, current_dir)
# Добавляем родительскую папку, где находится src
sys.path.insert(0, os.path.dirname(current_dir))

# Импортируем Base и модели
from fastapi_task2.src.infrastructure.sqlite.database import Base
from fastapi_task2.src.infrastructure.sqlite.models.user import User
from fastapi_task2.src.infrastructure.sqlite.models.post import Post
from fastapi_task2.src.infrastructure.sqlite.models.comment import Comment
from fastapi_task2.src.infrastructure.sqlite.models.category import Category
from fastapi_task2.src.infrastructure.sqlite.models.location import Location





config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()