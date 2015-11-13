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

    ref = Column(Integer, primary_key=True)
    organisation_ref = Column(Integer)
    code = Column(String(10))
    target_odscode = Column(String(10))
    org_odscode = Column(String(10))
    legal_start_date = Column(DateTime)
    legal_end_date = Column(DateTime)
    operational_start_date = Column(DateTime)
    operational_end_date = Column(DateTime)
    status = Column(String(10))
    uid = Column(String)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Relationships('%s %s %s %s %s %s %s %s %s %s %s'\
            )>" % (
            self.ref,
            self.organisation_ref,
            self.relationship_code,
            self.target_odscode,
            self.org_odscode,
            self.legal_start_date,
            self.legal_end_date,
            self.operational_start_date,
            self.operational_end_date,
            self.status,
            self.uid)
