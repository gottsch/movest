import requests
from bs4 import BeautifulSoup

from someguyssoftware.dao.earnings_dao import EarningsDao
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

    #
    # format of table being scrapped:
    # ---------------------------------------------------------------------------------------------
    # | Symbol | Company | Call Time | EPS Est. | Reported EPS | Surprise(%) |
    # ---------------------------------------------------------------------------------------------
    #
    def scrapeByDateRange(self, date1, date2):
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

                # create an earnings object
                e = Earnings(list_of_cells[EarningsService.SYMBOL_IDX],
                             list_of_cells[EarningsService.COMPANY_IDX],
                             list_of_cells[EarningsService.CALL_TIME_IDX],
                             list_of_cells[EarningsService.EPS_EST_IDX],
                             list_of_cells[EarningsService.REPORTED_EPS_IDX],
                             list_of_cells[EarningsService.SURPRISE_IDX],
                             dt.strftime("%Y-%m-%d"))
                print(e.tostring())

                # TODO add each element to a map keyed on the symbol+date
                # TODO build a query to check which earnings already exist
                # TODO

                #map example
                numbers = (1, 2, 3, 4)
                result = map(lambda x: x + x, numbers)
                print(list(result))

                self.dao.session.add(e)

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

    def getByDateRange(self, date1, date2):
        return self.dao.findByDateRange(self, date1, date2)

    def getByAsset(self, asset, year):
        return self.dao.findByAsset(self, asset, year)