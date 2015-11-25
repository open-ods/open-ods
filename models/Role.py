from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sys
import os.path

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.base import Base


class Role(Base):
    """
    Roles class that keeps track of information about a
    particular Roles. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'roles'

    ref = Column(Integer, primary_key=True)
    organisation_ref = Column(String)
    org_odscode = Column(String(10))
    code = Column(String(10))
    primary_role = Column(Boolean)
    unique_id = Column(String(10))
    status = Column(String(10))
    legal_start_date = Column(DateTime)
    legal_end_date = Column(DateTime)
    operational_start_date = Column(DateTime)
    operational_end_date = Column(DateTime)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Role(' %s %s %s %s %s %s %s %s %s %s %s')>" % (
            ref,
            organisation_ref,
            org_odscode,
            code,
            primary_role,
            unique_id,
            status,
            legal_start_date,
            legal_end_date,
            operational_start_date,
            operational_end_date)
