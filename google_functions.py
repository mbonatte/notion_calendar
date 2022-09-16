#https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
import datetime
import pickle
import os.path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events.owned']
#SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'google_credentials.json'

def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('google_token.pickle'):
       with open('google_token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, SCOPES)
         creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('google_token.pickle', 'wb') as token:
         pickle.dump(creds, token)
   try:
      service = build('calendar', 'v3', credentials=creds)
   except HttpError as error:
        print('An error occurred when trying to connect to Google service:')
        print(error)
        print()
   return service


def is_date(date):
   try:
      datetime.datetime.strptime(date, '%Y-%m-%d')
      return True
   except ValueError:
      return False
      

def is_date_time(date):
   try:
      datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f0%z')
      return True
   except ValueError:
      return False
   

def create_event_google_calendar(calendar_id = 'primary',
                                 summary = None,
                                 description = None,
                                 location = None,
                                 start = None,
                                 end = None,
                                 ):
   event = {
           "summary": summary,
           'location': location,
           "description": description,
           "reminders": {"useDefault": False,
                         "overrides": [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                            {'method': 'popup', 'minutes': 60}
                            ]
                        }
           }
   if is_date(start):
      event["start"]= {"date": start}
   elif is_date_time(start):
      event["start"]= {"dateTime": start}
   if end is None:
      end = start
   if is_date(start):
      event["end"]= {"date": end}
   elif is_date_time(start):
      event["end"]= {"dateTime": end}

   service = get_calendar_service()
   event_created = service.events().insert(calendarId=calendar_id,
                                           body=event).execute()

   print("Event created on Google Calendar")
   print("id: ", event_created['id'])
   print("summary: ", event_created['summary'])
   print()
   return event_created['id']



def list_events_google_calendar():
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List o 10 events')
   events_result = service.events().list(
       calendarId='primary', timeMin=now,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       print('No upcoming events found.')
   for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'])


def list_calendars_google_calendar():
   service = get_calendar_service()
   # Call the Calendar API
   print('Getting list of calendars')
   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
       print('No calendars found.')
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))
   return calendars
