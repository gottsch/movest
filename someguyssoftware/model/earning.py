from someguyssoftware.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from datetime import datetime, timedelta, date

#
#
# ----------------------------------------------------------------------
class Earnings(Base):
    def __init__(self, symbol, company, callTime, estimateEPS, reportedEPS, surprise, earningsDate):
        self.symbol = symbol
        self.company = company
        self.callTime = callTime
        self.estimateEPS = estimateEPS
        self.reportedEPS = reportedEPS
        self.surprise = surprise
        self.earningsDate = earningsDate

    def tostring(self):
        return "Earnings = [symbol: " + self.symbol \
               + ", company: " + self.company \
               + ", date: " + self.earningsDate \
               + ", call time: " + self.callTime \
               + ", estimate EPS: " + ("-" if self.estimateEPS is None else self.estimateEPS) \
               + ", reported EPS: " + ("-" if self.reportedEPS is None else self.reportedEPS) \
               + ", surprise: " + ("-" if self.surprise is None else self.surprise) \
               + "]"

    # db mapping/properties
    __tablename__ = 'earnings'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10))
    company = Column(String(75))
    callTime = Column("call_time", String(50))
    estimateEPS = Column("estimate_eps", DECIMAL(5,2))
    reportedEPS = Column("reported_eps", DECIMAL(5,2))
    surprise = Column("surprise", DECIMAL(5,2))
    earningsDate = Column("earnings_dt", DateTime, default=datetime.utcnow)

# ----------------------------------------------------------------------