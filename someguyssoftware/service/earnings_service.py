import requests
from bs4 import BeautifulSoup
from sqlalchemy import exc

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
                    self.assetService.save(asset)

                # print("Asset -> ", asset.tostring())
                # create an earnings object
                # NOTE have to create the asset first because earnings now has foreign key to asset
                e = Earnings(asset,
                             dt.strftime("%Y-%m-%d"),
                             # list_of_cells[EarningsService.COMPANY_IDX],
                             list_of_cells[EarningsService.CALL_TIME_IDX],
                             list_of_cells[EarningsService.EPS_EST_IDX],
                             list_of_cells[EarningsService.REPORTED_EPS_IDX],
                             list_of_cells[EarningsService.SURPRISE_IDX]
                             )
                #print(e.tostring())

                # TODO add each element to a map keyed on the symbol+date instead of just symbol
                # TODO will prevent collisions are bigger date ranges where multiple earnings for the same symbol could appear
                earningsMap[e.asset.symbol] = e

            # get a list of keys from the earnings dict
            keys = list(earningsMap.keys())

            # provide keys to query existing earnings records
            existingEarnings = self.getByDateRange(date1, date2, keys)

            # process each earnings
            for key, value in earningsMap.items():
                # if existing is empty or doesn't contain the earnings
                if not existingEarnings or not any(x.asset.symbol == key for x in existingEarnings):
                    print("Adding earnings -> ", value.asset.symbol)
                    self.dao.session.add(value)
                else:
                    # get the existing earnings
                    ee = next((x for x in existingEarnings if x.asset.symbol == key), None)
                    if (ee is not None):
                        print("Updating earnings -> ", value.asset.symbol)
                        # update the existing with what was pulled in.
                        ee.update(value)
                        self.dao.session.add(ee)

            # commit the inserts after each row
            try:
                self.dao.session.commit()
            except exc.SQLAlchemyError:
                print("an error occurred committing the session.")
                self.dao.session.rollback()
                return

            # clear all the lists, maps
            list_of_cells.clear()
            list_of_rows.clear()
            earningsMap.clear()

    #
    def getByID(self, id):
        return self.dao.findByID(id)

    def getByDateRange(self, date1, date2, assets=None):
        return self.dao.findByDateRange(date1, date2, assets)

    def getByAsset(self, asset, year):
        return self.dao.findByAsset(self, asset, year)