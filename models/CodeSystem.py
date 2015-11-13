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

    codesystem_name = Column(String(50))
    codesystem_id = Column(String(10))
    codesystem_displayname = Column(String(200))

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<CodeSystems(codesystem_name='%s',\
            codesystem_id='%s',\
            codesystem_displayname='%s'\
            )>" % (
            self.codesystem_name,
            self.codesystem_id,
            self.codesystem_displayname)
