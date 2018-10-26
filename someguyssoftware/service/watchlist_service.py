from someguyssoftware.dao.watchlist_dao import WatchListDao

#
class WatchListService:
    def __init__(self, session):
        self.dao = WatchListDao(session)

    #
    def getByID(self, id):
        return self.dao.findByID(id)

    def getAll(self):
        return self.dao.findAll()