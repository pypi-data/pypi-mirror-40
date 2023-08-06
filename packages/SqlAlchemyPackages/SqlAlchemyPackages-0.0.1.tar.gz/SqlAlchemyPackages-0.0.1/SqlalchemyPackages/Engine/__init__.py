from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tutorial.db')
Base = declarative_base()
session = sessionmaker(bind=engine)
Session = session()
