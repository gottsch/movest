from someguyssoftware.model.asset import Asset

#
class AssetDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Asset).get(id)

    def findBySymbol(self, symbol):
        return self.session.query(Asset).filter(Asset.symbol == symbol).one_or_none()
