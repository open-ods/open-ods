from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Relationships(Base):
    """
    Relationships class that keeps track of information about a
    particular Relationships. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'relationships'

    version_ref = Column(String)
    organisation_ref = Column(String)
    org_odscode = Column(String)
    target_odscode = Column(String)
    relationship_code = Column(String)

    # TODO: implement so a return is formatted nicely
    def __repr__(self):
        return "<Relationships(ref='%s', organisation_ref='%s',\
            org_odscode='%s',\
            target_odscode='%s',relationship_code='%s')>" % (
            self.version_ref,
            self.organisation_ref,
            self.org_odscode,
            self.target_odscode,
            self.relationship_code)
