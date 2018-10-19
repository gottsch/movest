import requests
from bs4 import BeautifulSoup

from someguyssoftware.service.asset_service import AssetService
from someguyssoftware.dao.earnings_dao import EarningsDao
from someguyssoftware.model.asset import Asset
from someguyssoftware.model.earning import Earnings

from someguyssoftware.util import date_helper

base_url = 'https://finance.yahoo.com/calendar/earnings?day='

#
class EarningsService:
    SYMBOL_IDX = 0
    COMPANY_IDX = 1
    CALL_TIME_IDX = 2
    EPS_EST_IDX = 3
    REPORTED_EPS_IDX = 4
    SURPRISE_IDX = 5

    def __init__(self, session):
        self.dao = EarningsDao(session)
        self.assetService = AssetService(session)

    #
    # format of table being scrapped:
    # ---------------------------------------------------------------------------------------------
    # | Symbol | Company | Call Time | EPS Est. | Reported EPS | Surprise(%) |
    # ---------------------------------------------------------------------------------------------
    #
    def scrapeByDateRange(self, date1, date2):
        earningsMap = dict()

        for dt in date_helper.daterange(date1, date2):
            print("Processing date -> " + dt.strftime("%Y-%m-%d"))

            url = base_url  + dt.strftime("%Y-%m-%d")
            response = requests.get(url)
            html = response.content

            # beautify the html
            soup = BeautifulSoup(html, features='html.parser')
            # extract the table that has class="data-table..."
            table = soup.find('table', attrs={'class': 'data-table'})
            if table is None: continue
            # print(table)
            list_of_rows = []
            # for each <tr>
            for row in table.findAll('tr')[1:]:
                list_of_cells = []
                # for each <td>
                for cell in row.findAll('td'):
                    # replace any nbsp; with empty string
                    text = cell.text.replace('&nbsp;', '')
                    # add all the cells into a list
                    list_of_cells.append(text)

                # add all the lists of cells into a list
                list_of_rows.append(list_of_cells)

                # validate data
                if list_of_cells[EarningsService.EPS_EST_IDX] == "-":
                    list_of_cells[EarningsService.EPS_EST_IDX] = None
                if list_of_cells[EarningsService.REPORTED_EPS_IDX] == "-":
                    list_of_cells[EarningsService.REPORTED_EPS_IDX] = None
                if list_of_cells[EarningsService.SURPRISE_IDX] == "-":
                    list_of_cells[EarningsService.SURPRISE_IDX] = None

                # get asset
                print("Searching for asset ->", list_of_cells[EarningsService.SYMBOL_IDX])
                asset = self.assetService.getBySymbol(list_of_cells[EarningsService.SYMBOL_IDX])
                if (asset is None):
                    # create a new asset
                    asset = Asset(list_of_cells[EarningsService.SYMBOL_IDX], list_of_cells[EarningsService.COMPANY_IDX])
                    # TODO create service & dao calls to add the asset and commit (as well as nonTx version)
                    self.assetService.dao.session.add(asset)
                    self.assetService.dao.session.commit()

                print("Asset -> ", asset.tostring())
                # create an earnings object
                # have to create the asset first because earnings now has foreign key to asset
                e = Earnings(asset,
                             dt.strftime("%Y-%m-%d"),
                             # list_of_cells[EarningsService.COMPANY_IDX],
                             list_of_cells[EarningsService.CALL_TIME_IDX],
                             list_of_cells[EarningsService.EPS_EST_IDX],
                             list_of_cells[EarningsService.REPORTED_EPS_IDX],
                             list_of_cells[EarningsService.SURPRISE_IDX]
                             )
                print(e.tostring())

                # TODO add each element to a map keyed on the symbol+date
                earningsMap[e.asset.symbol] = e

                # TODO build a query to check which earnings already exist
                # TODO


                # dict are equiv to map

                #self.dao.session.add(e)

            # get a list of keys from the earnings dict
            keys = list(earningsMap.keys())

            # provide keys to query existing earnings records
            existingEarnings = self.dao.getByDateRange(date1, date2, keys)
            print(existingEarnings)

            # commit the inserts after each row
            self.dao.session.commit()

        # TODO get html from web and beautify
        # TODO create a list of earnings objects / map by IDs
        #TODO check if the underlying asset exists for each earning
        # TODO pull all earnings by list of ID
        # TODO is historical, then update
        # TODO is non-existent add to DB
        # TODO if earnings asset is in watchlist, then add to calendar

    #
    def getByID(self, id):
        return self.dao.findByID(id)

    def getByDateRange(self, date1, date2, assets=None):
        return self.dao.findByDateRange(self, date1, date2, assets)

    def getByAsset(self, asset, year):
        return self.dao.findByAsset(self, asset, year)