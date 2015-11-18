from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Settings(Base):
    """
    Settings class that keeps track of information about a
    particular Settings. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'settings'

    key = Column(String(20), primary_key=True)
    value = Column(String(200))

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Settings('%s %s')>" % (
            self.key,
            self.value)
