from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Roles(Base):
    """
    Roles class that keeps track of information about a
    particular Roles. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'roles'

    version_ref = Column(String)
    organisation_ref = Column(String)
    org_odscode = Column(String)
    role_code = Column(String)

    # TODO: implement so a return is formatted nicely
    def __repr__(self):
        return "<Roles(ref='%s', organisation_ref='%s',\
            org_odscode='%s', role_code='%s')>" % (
            self.version_ref,
            self.organisation_ref,
            self.org_odscode,
            self.role_code)
