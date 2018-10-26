from someguyssoftware.model.watchlist import WatchList

from sqlalchemy import func

#
class WatchListDao():
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(WatchList).get(id)

    def findByName(self, name):
        return self.session.query(WatchList).filter(func.lower(WatchList.name) == func.lower(name)).one_or_none()
# .with_entities(models.User.username).

    def findAllAssets(self):
        return self.session.query()

    def findAll(self):
        return self.session.query(WatchList).all()