import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sqlite_file_name = '../database.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))

DATABASE_URL = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}'

engine = create_engine(DATABASE_URL)


Session = sessionmaker(engine)
Base = declarative_base()