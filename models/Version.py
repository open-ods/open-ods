from sqlalchemy import Column, Integer, String
import sys
import os.path

# setup path so we can import our own models and controllers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.base import Base


class Version(Base):
    """Versions class that keeps track of information about a
    particular ods file update. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'versions'

    version_ref = Column(Integer, primary_key=True)
    import_timestamp = Column(String)
    file_version = Column(String)
    publication_seqno = Column(String)
    publication_date = Column(String)
    publication_type = Column(String)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Version(ref='%s',\
            import_timestamp='%s',\
            file_version='%s',\
            publication_seqno='%s',\
            publication_date='%s',\
            publication_type='%s'\
            )>" % (
            self.version_ref,
            self.import_timestamp,
            self.file_version,
            self.publication_seqno,
            self.publication_date,
            self.publication_type)
