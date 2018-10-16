import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

from someguyssoftware.model.base import Base
from someguyssoftware.model.task import Task

response = requests.get("http://www.google.com")
html = response.content
print(html)

engine = create_engine('mysql+mysqlconnector://root:fungible@localhost/movest')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

t = Task("myTask", status="hi")
print(t.tostring())


