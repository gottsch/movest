from someguyssoftware.model.base import Base, association_table
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields

#
class Asset(Base):
    def __init__(self, symbol, company):
        self.symbol = symbol
        self.company = company

    # db mapping/properties
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(45))
    company = Column(String(75))
    watchLists = relationship(
        "WatchList",
        secondary=association_table,
        back_populates="assets")

    # java-style
    def tostring(self):
        return "Asset = [id:" + str(self.id) \
            + ", symbol: '" + self.symbol \
            + "', company: '" + str(self.company) \
            + "']"

    # python-style
    def __repr__(self):
        return "<Asset(symbol='%s', company='%s')>" % (self.symbol , self.company)

    #
    def to_json(self):
        d = dict()
        d['id'] = self.id
        d['symbol'] = self.symbol
        d['company'] = self.company
        return d


class AssetSchema(Schema):
    id = fields.Number()
    symbol = fields.Str()
    company = fields.Str()