from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.Base import Base

url = "postgresql://{}:{}@{}:{}/{}".format(
environ.get("POSTGRES_USER"),
environ.get("POSTGRES_PASSWORD"),
environ.get("POSTGRES_HOST"),
environ.get("POSTGRES_PORT"),
environ.get("POSTGRES_NAME")
)

engine = create_engine(url)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
