# a repositories engine is a software component that provides an interface between your
# application and a repositories. It provides a way for your application to communicate with
# the repositories. In summary, a repositories engine is a software component that manages the
# storage and retrieval of data in a repositories, providing an interface for your application
# to interact with the repositories.
import os

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine

# It provides a set of common functionality and conveniences for defining repositories models.
from sqlalchemy.ext.declarative import declarative_base

# The sessionmaker class is a factory class that is used to create new sessions, which are
# used to interact with the repositories.
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # In case service brings up with docker.
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_CLOUD = os.getenv("DB_CLOUD")  # This is defined only on the Cloud Run
    if DB_CLOUD:
        # https://cloud.google.com/sql/docs/postgres/connect-run#console
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>?unix_sock=<INSTANCE_UNIX_SOCKET>
        # f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{DB_CLOUD}"

        # f"postgresql+psycopg2://postgres:postgres@/{DB_NAME}?host=/cloudsql/{DB_CLOUD}"
        # f"postgresql+psycopg2://postgres:postgres@/percentdb?host=/cloudsql/percentpassed:us-central1:percent"
        # DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@/{DB_NAME}?host=/cloudsql/{DB_CLOUD}"  # noqa
        DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@/{DB_NAME}?host=/cloudsql/percentpassed:us-central1:percent"
    else:
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()


templates = Jinja2Templates(directory="templates")
