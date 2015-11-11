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

    version_ref = Column(String, primary_key=True)
    codesystem_name = Column(String)
    codesystem_id = Column(String)
    codesystem_displayname = Column(String)

    # TODO: implement so a return is formatted nicely
    def __repr__(self):
        return "<CodeSystems(ref='%s', codesystem_name='%s',\
            codesystem_id='%s', codesystem_displayname='%s',\
            publication_date='%s',publication_type='%s')>" % (
            self.version_ref,
            self.codesystem_name,
            self.codesystem_id,
            self.codesystem_displayname,
            self.publication_date,
            self.publication_type)
