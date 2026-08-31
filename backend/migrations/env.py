"""Alembic async migration environment."""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from backend.app.database import Base
from backend.app.config import settings

target_metadata = Base.metadata
