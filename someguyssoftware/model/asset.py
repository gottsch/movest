from someguyssoftware.model.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

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

    # java-style
    def tostring(self):
        return "Asset = [symbol: '" + self.symbol \
            + "', company: '" + str(self.company) \
            + "']"

    # python-style
    def __repr__(self):
        return "<Asset(symbol='%s', company='%s')>" % (self.name , self.company)