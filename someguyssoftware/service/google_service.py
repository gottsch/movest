from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import configparser

# TODO for now use module global as I don't know how to make it a global or available from a context
# get the config file
config = configparser.RawConfigParser()
config.read("someguyssoftware/config/movest.properties")


# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'

class GoogleService():
    def addEarningsToCalendar(self, earnings):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('cal-creds.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        # add event to calendar
        event = {
            'summary': earnings.asset.symbol + " Earnings",
            'location': '',
            'description': earnings.callTime,
            'start': {
                'dateTime': str(earnings.earningsDate) + 'T09:00:00-04:00',
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': str(earnings.earningsDate) + 'T09:30:00-04:00',
                'timeZone': 'America/New_York',
            }
            #,
            #'attendees': [
            #   {'email': 'mark.gottschling@gmail.com'}
            #]
        }

        event = service.events().insert(calendarId = config.get('Google', 'calendar.id'), body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))