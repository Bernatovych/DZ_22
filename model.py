from sqlalchemy import Date
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    records_id = Column(Integer, ForeignKey('records.id', ondelete='CASCADE'))
    records = relationship("Records", back_populates="phones")


class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    records_id = Column(Integer, ForeignKey('records.id', ondelete='CASCADE'))
    records = relationship("Records", back_populates="notes")
    tags = relationship("Tags", back_populates="notes", passive_deletes='all')


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    notes_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'))
    notes = relationship("Notes", back_populates="tags")


class Addresses(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    records_id = Column(Integer, ForeignKey('records.id', ondelete='CASCADE'))
    records = relationship("Records", back_populates="addresses")


class Emails(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    records_id = Column(Integer, ForeignKey('records.id', ondelete='CASCADE'))
    records = relationship("Records", back_populates="emails")


class Records(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(String)
    phones = relationship("Phones", back_populates="records", passive_deletes='all')
    notes = relationship("Notes", back_populates="records", passive_deletes='all')
    addresses = relationship("Addresses", back_populates="records", passive_deletes='all')
    emails = relationship("Emails", back_populates="records", passive_deletes='all')


engine = create_engine("sqlite:///address_book.db", pool_pre_ping=True)

Session = sessionmaker(bind=engine)
session = Session()

