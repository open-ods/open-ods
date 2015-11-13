from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
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

    role_ref = Column(Integer, primary_key=True)
    organisation_ref = Column(String)
    org_odscode = Column(String(10))
    role_code = Column(String(10))
    primary_role = Column(Boolean)
    role_unique_id = Column(String(10))
    role_status = Column(String(10))
    role_legal_start_date = Column(DateTime)
    role_legal_end_date = Column(DateTime)
    role_operational_start_date = Column(DateTime)
    role_operational_end_date = Column(DateTime)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Roles(\
            role_ref='%s', \
            organisation_ref='%s', \
            org_odscode='%s', \
            role_code='%s', \
            primary_role='%s', \
            role_unique_id='%s', \
            role_status='%s', \
            role_legal_start_date='%s', \
            role_legal_end_date='%s', \
            role_operational_start_date='%s', \
            role_operational_end_date='%s' \
            )>" % (
            role_ref,
            organisation_ref,
            org_odscode,
            role_code,
            primary_role,
            role_unique_id,
            role_status,
            role_legal_start_date,
            role_legal_end_date,
            role_operational_start_date,
            role_operational_end_date)
