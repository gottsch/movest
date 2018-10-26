from someguyssoftware.model.earning import Earnings
from someguyssoftware.model.asset import Asset

#
class EarningsDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Earnings).get(1)

    def findByDateRange(self, date1, date2, assets = None):
        pass # TODO
        if (assets is None):
            earnings = self.session.query(Earnings).all()
        else:
            earnings = self.session.query(Earnings)\
                .join(Asset, Asset.id == Earnings.asset_id) \
                .filter(Asset.symbol.in_(assets)) \
                .filter(Earnings.earningsDate >= date1) \
                .filter(Earnings.earningsDate <= date2) \
                .all()

        return earnings

    #
    def findByAsset(self, asset, year):
        pass # TODO