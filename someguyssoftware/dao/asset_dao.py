from someguyssoftware.model.asset import Asset

#
class AssetDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Asset).get(id)

    def findBySymbol(self, symbol):
        return self.session.query(Asset).filter(Asset.symbol == symbol).one_or_none()

    def findAllWatched(self):
        return self.session.query(Asset).filter(Asset.watchLists != None).all()


    def save(self, asset):
        self.session.add(asset)
        self.session.flush()
        return asset

    def saveNoTx(self, asset):
        self.session.add(asset)
        return asset
