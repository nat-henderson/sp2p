from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, json

props = None
with open(os.path.expanduser('~/.sp2p/propfile')) as f: props = json.loads(f.read())
engine = create_engine(props['protocol'] + '://' +props['username'] + ':' + props['password'] + '@' +
        props['host'] + '/' + props['database'])

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key = True)
    secret = Column(String(50))
    lastping = Column(DateTime())
    lastip = Column(String(17))
    lastport = Column(Integer())

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer(), primary_key = True)
    filename = Column(String(120))
    md5 = Column(String(32))

class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer(), primary_key = True)
    owner = Column(String(50), ForeignKey('users.id'))
    filename = Column(String(120), ForeignKey('files.filename'))
    dirpath = Column(String(150))

if __name__ == "__main__":
    Base.metadata.drop_all()
    Base.metadata.create_all()

