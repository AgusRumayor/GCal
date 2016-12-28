from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import pytz

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('.')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    remember_hours =1
    #From this time to 1 hour later - 5 minutes (trying avoid duplicates messages
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=remember_hours)
    now_1_hour = now+datetime.timedelta(hours=remember_hours) - datetime.timedelta(minutes=5)
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = now.isoformat() + 'Z'
    now_1_hour = now_1_hour.isoformat() +'Z'
    
    calendars = ['ad8kj3tgp3udd0unsvrde4p5hc8gs01p@import.calendar.google.com', 
                 '84v648v1lo7sp9dqrj8egfe8b6m9qg83@import.calendar.google.com', 
		 '30qd3ak2qrk0leu1sjl7rb72jf55r4bt@import.calendar.google.com', 
		 '9trsej2tkp3t4jtp51i602ifce6sep2u@import.calendar.google.com',
		 'a1nvjeb8qbs6d496aeo84i43r8@group.calendar.google.com']
    events = []
    for calendar in calendars:
    	eventsResult = service.events().list(
            calendarId=calendar, timeMin=now, timeMax=now_1_hour, singleEvents=True,
            orderBy='startTime').execute()
    	events = events + eventsResult.get('items', [])
    
    for event in events:
	if 'description' in event:
	    details = event['description'].split('\n')
	    for detail in details:
		detail = detail.strip()
	        if "Name:" in detail:
	    	    client= (detail.split(':')[1]).strip()
		if "Phone:" in detail:
		    phone= (detail.split(':')[1]).strip()
	    if 'client' in locals() and 'phone' in locals():
	        print('{0}:"Hola, Te recordamos que hoy tienes cita con nosotros, nos dara gusto verte, Clinica Piezzo"'.format(phone, client))


if __name__ == '__main__':
    main()
