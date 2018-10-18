from someguyssoftware.model.base import Base
from someguyssoftware.model.asset import Asset

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Table
from sqlalchemy.orm import relationship, backref

# the association table between watch_list and assets (where watch_list is the parent)
association_table = Table('watch_list_assets', Base.metadata,
                          Column('watch_list_id', Integer, ForeignKey('watch_list.id')),
                          Column('asset_id', Integer, ForeignKey('assets.id'))
                          )

#
class WatchList(Base):
    def __init__(self,):
        pass

    # db mapping/properties
    __tablename__ = 'watch_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    assets = relationship("Asset", secondary=association_table)
