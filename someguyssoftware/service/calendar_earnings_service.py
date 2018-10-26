import requests
from bs4 import BeautifulSoup
from sqlalchemy import exc

from someguyssoftware.dao.calendar_earnings_dao import CalendarEarningsDao
from someguyssoftware.service.asset_service import AssetService
from someguyssoftware.service.watchlist_service import WatchListService
from someguyssoftware.service.earnings_service import EarningsService
from someguyssoftware.service.asset_service import AssetService
from someguyssoftware.service.google_service import GoogleService

from someguyssoftware.dao.earnings_dao import EarningsDao
from someguyssoftware.model.asset import Asset
from someguyssoftware.model.earning import Earnings
from someguyssoftware.model.calendar_earnings import CalendarEarnings

from someguyssoftware.util import date_helper

base_url = 'https://finance.yahoo.com/calendar/earnings?day='

#
class CalendarEarningsService:
    def __init__(self, session):
        self.dao = CalendarEarningsDao(session)
        self.watchListService = WatchListService(session)
        self.assetService = AssetService(session)
        self.earningsService = EarningsService(session)
        self.googleService = GoogleService()

    #
    def getByID(self, id):
        return self.dao.findByID(id)

    def getBySymbol(self, symbol, date1, date2):
        return self.dao.findBySymbol(symbol, date1, date2)

    def updateFromEarnings(self, date1, date2):
        # get all watched assets
        watchedAssets = self.assetService.getAllWatch()
        print("watched -> ", watchedAssets)
        # convert to list
        waList = list()
        for wa in watchedAssets:
            waList.append(wa.symbol)
        print("wa list -> ", waList)
        # get all watched earnings in date range
        watchedEarnings = self.earningsService.getByDateRange(date1, date2, waList)
        print("watched earnings -> ", watchedEarnings)
        # get all watched calendar earnings
        watchedCalendarEarnings = self.getByDateRange(date1, date2, watchedEarnings)
        print("watched cal earnings -> ", watchedCalendarEarnings)

        #my_list = self.dao.findBySymbol("TLRY", date1, date2)
        #print("my_list -> ", my_list)

        # for every watched earnings, check if cal earnings exists AND that .calendar = true
        # else, add new cal earnings
        for we in watchedEarnings:
            # check if earnings is in watched cal earnings
            if not watchedCalendarEarnings or not any(x.earnings_id == we.id for x in watchedCalendarEarnings):
                print("Adding Calendar Earnings -> ", we)
                wce = CalendarEarnings()
                wce.earnings = we
                wce.earnings_id = we.id
                wce.calendar = True
                self.dao.session.add(wce)
                # TODO add to list
                self.googleService.addEarningsToCalendar(we)
            else:
                # get the existing earnings
                wce = next((x for x in watchedCalendarEarnings if x.earnings_id == we.id and x.calendar == 0), None)
                if (wce is not None):
                    print("Updating calendar earnings -> ", we)
                    wce.calendar = True
                    self.dao.session.add(wce)
                    # TODO add to list
                    self.googleService.addEarningsToCalendar(we)

            # TODO for all in add list, add to google calendar

            # persist changes
            self.dao.session.commit()


    def getByDateRange(self, date1, date2, earnings=None):
        return self.dao.findByDateRange(date1, date2, earnings)