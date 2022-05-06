from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Stats(Base):
    """ Processing Statistics """
    __tablename__ = "getdata"

    id = Column(Integer,primary_key=True) 
    windows_percent = Column(Integer,nullable=True)
    mac_percent = Column(Integer, nullable=True)

    def __init__(self, windows_percent, mac_percent):
        """ Initializes a processing statistics objet """
        self.windows_percent = windows_percent
        self.mac_percent = mac_percent

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['windows_percent'] = self.windows_percent
        dict['mac_percent'] = self.mac_percent

        return dict