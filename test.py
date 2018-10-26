import requests
from datetime import datetime, timedelta, date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from someguyssoftware.model.base import Base
from someguyssoftware.model.task import Task
from someguyssoftware.model.asset import Asset
from someguyssoftware.model.watchlist import WatchList, WatchListSchema
from someguyssoftware.model.earning import Earnings
from someguyssoftware.dao.asset_dao import AssetDao
from someguyssoftware.dao.watchlist_dao import WatchListDao

from someguyssoftware.service.asset_service import AssetService
from someguyssoftware.service.earnings_service import EarningsService
from someguyssoftware.service.calendar_earnings_service import CalendarEarningsService


import sys

# TODO don't need to do this.... just get todays date and create a range from now-1 to now +  30
print('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print("arg[1] -> ", sys.argv[1])

format_str = '%m-%d-%Y' # The format
datetime_obj = datetime.strptime(sys.argv[1], format_str)
print("datetime obj of arg[1] -> ", datetime_obj.date())

today = date.today()
yesterday = today - timedelta(days=1)
to30day = today + timedelta(days=30)
print("days from ", yesterday, " <--> ", to30day)

#response = requests.get("http://www.google.com")
#html = response.content
#print(html)

engine = create_engine('mysql+mysqlconnector://root:fungible@localhost/movest')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

#t = Task("myTask", status="hi")
#print(t.tostring())
#print(t.__repr__())

#asset = session.query(Asset).get(1)
assetDao = AssetDao(session)
#asset = assetDao.findByID(1)
assetService = AssetService(session)
#asset = assetService.getByID(1)
#print(asset.tostring())

#e = Earnings(asset, "2018-10-16")
#session.add(e)
wl = WatchList()
wl.name = "Weed"
#wl.assets.append(asset)
#session.add(wl)

# get the earnings service
earningsService = EarningsService(session)

# scrape website, adding/updating earnings for date range
d1 = date(2018, 10, 28)
d2 = date(2018, 10, 28)
#earningsService.scrapeByDateRange(d1, d2)

# TODO if earnings asset is in watchlist, then add to calendar
# update calendar with watchlist earnings
#calendarService = CalendarEarningsService(session)
#calendarService.updateFromEarnings(d1, d2)

session.commit()
#wldao = WatchListDao(session)
#wl = wldao.findByName("Weed") # <-- TODO should use ilike instead of ==
#print("WatchList -> ", wl.__repr__())
session.close()




