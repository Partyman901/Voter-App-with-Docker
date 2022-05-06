from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Data(Base):
    """ Processing Statistics """
    __tablename__ = "enterdata"

    id = Column(Integer,primary_key=True) 
    windows = Column(Integer,nullable=True)
    mac = Column(Integer, nullable=True)

    def __init__(self, windows, mac):
        """ Initializes a processing statistics object """
        self.windows = windows
        self.mac = mac

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['windows'] = self.windows
        dict['mac'] = self.mac

        return dict