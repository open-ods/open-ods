from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Organisation(Base):
    """
    Organisations class that keeps track of information about a
    particular organisations. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'organisations'

    organisation_ref = Column(Integer, primary_key=True)
    org_odscode = Column(String(10))
    org_name = Column(String(200))
    org_status = Column(String(10))
    org_recordclass = Column(String(10))
    org_lastchanged = Column(DateTime)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Organisations(\
            ref='%s',\
            org_odscode='%s',\
            org_name='%s',\
            org_status='%s',\
            org_recordclass='%s',\
            org_lastchanged='%s'\
            )>" % (
            self.organisation_ref,
            self.org_odscode,
            self.org_name,
            self.org_status,
            self.org_recordclass,
            self.org_lastchanged)
