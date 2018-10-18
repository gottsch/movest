import requests
from datetime import datetime, timedelta, date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from someguyssoftware.model.base import Base
from someguyssoftware.model.task import Task
from someguyssoftware.model.asset import Asset
from someguyssoftware.model.watchlist import WatchList
from someguyssoftware.model.earning import Earnings
from someguyssoftware.dao.asset_dao import AssetDao
from someguyssoftware.service.asset_service import AssetService
from someguyssoftware.service.earnings_service import EarningsService

response = requests.get("http://www.google.com")
html = response.content
print(html)

engine = create_engine('mysql+mysqlconnector://root:fungible@localhost/movest')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

t = Task("myTask", status="hi")
print(t.tostring())
print(t.__repr__())

#asset = session.query(Asset).get(1)
#assetDao = AssetDao(session)
#asset = assetDao.findByID(1)
assetService = AssetService(session)
asset = assetService.getByID(1)
print(asset.tostring())

#e = Earnings(asset, "2018-10-16")
#session.add(e)
#wl = WatchList()
#wl.name = "Weed"
#wl.assets.append(asset)
#session.add(wl)

earningsServce = EarningsService(session)
earningsServce.scrapeByDateRange(date(2018, 10, 15), date(2018, 10, 16))
session.commit()

