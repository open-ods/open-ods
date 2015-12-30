import sys

import os.path
from sqlalchemy import Column, Integer, String, Date, Boolean

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from openods_import.models.base import Base


class Organisation(Base):
    """
    Organisations class that keeps track of information about a
    particular organisations. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'organisations'

    ref = Column(Integer, primary_key=True)
    odscode = Column(String(10))
    name = Column(String(200))
    status = Column(String(10))
    record_class = Column(String(10))
    last_changed = Column(String)
    legal_start_date = Column(Date)
    legal_end_date = Column(Date)
    operational_start_date = Column(Date)
    operational_end_date = Column(Date)
    ref_only = Column(Boolean)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Organisation('%s %s %s %s %s %s %s %s %s %s %s'\)>" % (
            self.ref,
            self.odscode,
            self.name,
            self.status,
            self.record_class,
            self.last_changed,
            self.legal_start_date,
            self.legal_end_date,
            self.operational_start_date,
            self.operational_end_date,
            self.ref_only)
