from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
import sys
import os.path

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.base import Base


class Addresses(Base):
    """
    Addresses class that keeps track of information about a
    particular Addresses. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'addresses'

    addresses_ref = Column(Integer, primary_key=True)
    organisation_ref = Column(Integer)
    org_odscode = Column(String(10))
    street_address_line1 = Column(String)
    street_address_line2 = Column(String)
    street_address_line3 = Column(String)
    town = Column(String)
    county = Column(String)
    postal_code = Column(String)
    location_id = Column(String)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Addresses(%s %s %s %s %s %s %s %s %s %s\)>" \
            % (
                self.addresses_ref,
                self.organisation_ref,
                self.org_odscode,
                self.street_address_line1,
                self.street_address_line2,
                self.street_address_line3,
                self.town,
                self.county,
                self.postal_code,
                self.location_id)
