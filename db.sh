CREATE DATABASE percent;

GRANT ALL PRIVILEGES ON DATABASE percent TO karim;

ALTER DATABASE percent RENAME TO percentdb;
ALTER TABLE residence ADD COLUMN city character varying;

# alembic commands:
alembic init alembic

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head