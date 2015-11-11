from sqlalchemy import Column, ForeignKey, Integer, String
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

    organisation_ref = Column(String)
    org_odscode = Column(String)
    org_name = Column(String)
    org_status = Column(String)
    org_recordclass = Column(String)
    org_lastchanged = Column(String)

    # TODO: implement so a return is formatted nicely
    def __repr__(self):
        return "<Organisations(ref='%s', org_odscode='%s',\
            org_name='%s', org_status='%s',\
            org_recordclass='%s',org_lastchanged='%s')>" % (
            self.organisation_ref,
            self.org_odscode,
            self.org_name,
            self.org_status,
            self.org_recordclass,
            self.org_lastchanged)
