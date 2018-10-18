from someguyssoftware.model.earning import Earnings

#
class EarningsDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Earnings).get(1)

    def findByDateRange(self, date1, date2):
        pass # TODO

    def findByAsset(self, asset, year):
        pass # TODO