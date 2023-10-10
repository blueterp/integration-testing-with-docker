"""User Model and ORM Table"""
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry

from models.user import User


mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50), unique=True),
    Column("fullname", String(50)),
)


mapper_registry.map_imperatively(User, user_table)
