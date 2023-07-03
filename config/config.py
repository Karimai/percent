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

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()


templates = Jinja2Templates(directory="templates")
