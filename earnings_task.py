import logging
import configparser
from datetime import datetime, timedelta, date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from someguyssoftware.logging.util import create_rotating_log
from someguyssoftware.model.base import Base
from someguyssoftware.service.earnings_service import EarningsService
from someguyssoftware.service.calendar_earnings_service import CalendarEarningsService

# create a logger
create_rotating_log("C:/Users/mgottsch/PycharmProjects/movest/movest.log", "movest")
# get the logger
logger = logging.getLogger("movest")
logger.info("starting earnings task...")

# get the config file
config = configparser.RawConfigParser()
config.read("C:/Users/mgottsch/PycharmProjects/movest/someguyssoftware/config/movest.properties")

# connect to the database
engine = create_engine(config.get('DB', 'connection.url'))
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

# create the range to process (31 days)
today = date.today()
yesterday = today - timedelta(days=1)
future = today + timedelta(days=30)
print("days from ", yesterday, " <--> ", future)
logger.info("days: %s <--> %s" % (yesterday, future))

# get the earnings service
earningsService = EarningsService(session)

# scrape website, adding/updating earnings for date range
d1 = yesterday
d2 = future
earningsService.scrapeByDateRange(d1, d2)

# update calendar with watchlist earnings
calendarService = CalendarEarningsService(session)
calendarService.updateFromEarnings(d1, d2)

session.commit()
session.close()