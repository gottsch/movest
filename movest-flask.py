import configparser
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

from someguyssoftware.model.base import Base
from someguyssoftware.service.watchlist_service import WatchListService
from someguyssoftware.model.watchlist import WatchList, WatchListSchema

# get the config file
config = configparser.RawConfigParser()
config.read("C:/Users/mgottsch/PycharmProjects/movest/someguyssoftware/config/movest.properties")

# connect to the database
engine = create_engine(config.get('DB', 'connection.url'))
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

# services
wlService = WatchListService(session)

# create flask application
app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('overview'))

@app.route("/overview/")
@app.route("/overview/<name>")
def overview(name=None):
    if (name == None):
        return render_template("overview.html")
    else:
        x = request.args.get('x')
        #return "Overview"
        return render_template('overview.html', name=name + ":" + x)

@app.route("/rest/watchlists/", methods=["GET"])
def watchlists():
    list = wlService.getAll()

    # create a new list of json strings
    # t = [i.to_json() for i in list]
    # return json.dumps(t, indent=2)

    schema = WatchListSchema(many=True)
    x = schema.dump(list)
    return json.dumps(x.data, indent=2)


@app.route("/rest/watchlist/<id>", methods=["GET"])
def rest_watchlist_by_id(id):
    # TODO add error checking
    w = wlService.getByID(id)
    schema = WatchListSchema()
    return json.dumps(schema.dump(w).data)
    #return json.dumps(w.to_json(), indent=4)

@app.route("/watchlist/<id>", methods=["GET"])
def watchlist_by_id(id):
    w = wlService.getByID(id)
    return render_template("watchlist.html", watchlist = w)

@app.route("/watchlist/", methods=["POST"])
def add_watchlist():
    if (request.form):
        print(request.form)

    return "{'message': 'hi'}"

    #TODO on success redirect or just return JSON responses

"""
main method
"""
if __name__ == "__main__":
    app.run(debug=True)