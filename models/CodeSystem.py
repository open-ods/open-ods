from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CodeSystems(Base):
    """
    CodeSystems class that keeps track of information about a
    particular ods file update. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'codesystems'

    ref = Column(Integer, primary_key=True)
    name = Column(String(50))
    id = Column(String(10))
    displayname = Column(String(200))

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<CodeSystems('%s %s %s %s'\
            )>" % (
            self.ref,
            self.name,
            self.id,
            self.displayname)
