from someguyssoftware.model.asset import Asset
from someguyssoftware.dao.asset_dao import AssetDao

#
class AssetService:
    def __init__(self, session):
        self.dao = AssetDao(session)

    #
    def getByID(self, id):
        return self.dao.findByID(id)

    #
    def getBySymbol(self, symbol):
        return self.dao.findBySymbol(symbol)

    def getAllWatch(self):
        return self.dao.findAllWatched()

    #
    def save(self, asset):
        return self.dao.save(asset)