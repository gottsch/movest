from someguyssoftware.model.asset import Asset

#
class AssetDao:
    def __init__(self, session):
        self.session = session

    def findByID(self, id):
        return self.session.query(Asset).get(id)