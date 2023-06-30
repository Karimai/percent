CREATE DATABASE percent;

GRANT ALL PRIVILEGES ON DATABASE percent TO karim;

# alembic commands:
alembic init alembic

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head