from someguyssoftware.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

class CalendarEarnings(Base):
    def __init__(self):
        pass

    # db mapping/properties
    __tablename__ = 'calendar_earnings'
    id = Column(Integer, primary_key=True)
    earnings_id = Column(Integer, ForeignKey('earnings.id'))
    earnings = relationship("Earnings")
    calendar = Column(Boolean)


    # python-style
    def __repr__(self):
        return "<CalendarEarnings(id='%d', calendar='%s')>" % (self.id, str(self.calendar))
