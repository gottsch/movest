from someguyssoftware.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta, date

#
#
# ----------------------------------------------------------------------
class Earnings(Base):
    def __init__(self, asset, earningsDate, callTime=None, estimateEPS=None, reportedEPS=None, surprise=None):
        self.asset_id = asset.id
        self.asset = asset
        self.callTime = callTime
        self.estimateEPS = estimateEPS
        self.reportedEPS = reportedEPS
        self.surprise = surprise
        self.earningsDate = earningsDate

    def tostring(self):
        return "Earnings = [asset_id: " + self.asset_id \
               + ", date: " + self.earningsDate \
               + ", call time: " + self.callTime \
               + ", estimate EPS: " + ("-" if self.estimateEPS is None else self.estimateEPS) \
               + ", reported EPS: " + ("-" if self.reportedEPS is None else self.reportedEPS) \
               + ", surprise: " + ("-" if self.surprise is None else self.surprise) \
               + "]"

    # db mapping/properties
    __tablename__ = 'earnings'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relationship("Asset")

    earningsDate = Column("earnings_dt", DateTime, default=datetime.utcnow)
    callTime = Column("call_time", String(50))
    estimateEPS = Column("estimate_eps", DECIMAL(5,2))
    reportedEPS = Column("reported_eps", DECIMAL(5,2))
    surprise = Column("surprise", DECIMAL(5,2))

# ----------------------------------------------------------------------