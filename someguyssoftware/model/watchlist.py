from someguyssoftware.model.base import Base, association_table
from someguyssoftware.model.asset import Asset, AssetSchema

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Table
from sqlalchemy.orm import relationship, backref

from marshmallow import Schema, fields

#
class WatchList(Base):
    def __init__(self,):
        pass

    # db mapping/properties
    __tablename__ = 'watch_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    assets = relationship("Asset", secondary=association_table, back_populates="watchLists")


    # python-style
    def __repr__(self):
        return "<WatchList(name='%s')>" % self.name

    # create a dictionary of native values (ie not sqlalchemy properties ex Column())
    def to_json(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        # add all the assets
        a = [x.to_json() for x in self.assets]
        d['assets'] = a
        return d

"""

"""
class WatchListSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Number()
    name = fields.Str()
    assets = fields.List(fields.Nested(AssetSchema))
