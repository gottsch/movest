from someguyssoftware.model.earning import Earnings

#
class EarningsDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Earnings).get(1)

    def findByDateRange(self, date1, date2, assets = None):
        pass # TODO
        if (assets is None):
            self.session.query(Earnings)
        else:
            self.session.query(Earnings).filter(Earnings.asset.symbol.in_(assets)).all()

    def findByAsset(self, asset, year):
        pass # TODO