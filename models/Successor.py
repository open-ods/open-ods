from sqlalchemy import Column, Integer, String, Date
import sys
import os.path

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.base import Base


class Successor(Base):
    """
    Successor class that keeps track of information about successors for entities.
    This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'successors'

    ref = Column(Integer, primary_key=True)
    unique_id = Column(Integer)
    legal_start_date = Column(Date)
    type = Column(String(12))
    target_odscode = Column(String(10))
    target_primary_role_code = Column(String(10))
    target_unique_role_id = Column(String(10))

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Successor(%s %s %s %s %s %s %s\)>" \
            % (
                self.ref,
                self.unique_id,
                self.legal_start_date,
                self.type,
                self.target_odscode,
                self.target_primary_role_code,
                self.target_unique_role_id
               )
