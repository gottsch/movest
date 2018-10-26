from someguyssoftware.model.calendar_earnings import CalendarEarnings
from someguyssoftware.model.earning import Earnings
from someguyssoftware.model.asset import Asset

#
class CalendarEarningsDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(CalendarEarnings).get(id)

    def findBySymbol(self, symbol, date1, date2):
        print(self.session.query(CalendarEarnings)
            .join(Earnings, Earnings.id == CalendarEarnings.earnings_id)
            .join(Asset, Asset.id == Earnings.asset_id)
            .filter(Asset.symbol == symbol)
            .filter(Earnings.earningsDate >= date1)
            .filter(Earnings.earningsDate <= date2))
        earnings = self.session.query(CalendarEarnings) \
            .join(Earnings, Earnings.id == CalendarEarnings.earnings_id) \
            .join(Asset, Asset.id == Earnings.asset_id) \
            .filter(Asset.symbol == symbol) \
            .filter(Earnings.earningsDate >= date1) \
            .filter(Earnings.earningsDate <= date2).all()
        return earnings


    def findByDateRange(self, date1, date2, earnings = None):
        # build list of ids
        ids = list()
        for e in earnings:
            ids.append(e.id)

        if (earnings is None):
            cal_earnings = self.session.query(CalendarEarnings).all() # TODO finish
        else:
            cal_earnings = self.session.query(CalendarEarnings)\
                .join(Earnings, Earnings.id == CalendarEarnings.earnings_id) \
                .filter(Earnings.id.in_(ids)) \
                .filter(Earnings.earningsDate >= date1) \
                .filter(Earnings.earningsDate <= date2) \
                .all()

        return cal_earnings

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def saveNoTx(self, entity):
        self.session.add(entity)
        return entity
