from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Versions(Base):
    """Versions class that keeps track of information about a
    particular ods file update. This class uses SQLAlchemy as an ORM

    """
    __tablename__ = 'versions'

    version_ref = Column(String, primary_key=True)
    import_timestamp = Column(String)
    file_version = Column(String)
    publication_seqno = Column(String)
    publication_date = Column(String)
    publication_type = Column(String)

    # Returns a printable version of the objects contents
    def __repr__(self):
        return "<Version(ref='%s', import_timestamp='%s',\
            file_version='%s', publication_seqno='%s',\
            publication_date='%s',publication_type='%s')>" % (
            self.version_ref,
            self.import_timestamp,
            self.file_version,
            self.publication_seqno,
            self.publication_date,
            self.publication_type)
