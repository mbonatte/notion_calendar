import time
import json
from notion_functions import get_clean_data_from_notion
from google_functions import create_event_google_calendar, list_calendars_google_calendar
from functions import filter_by_tags, filter_by_time, save_event, is_event_new
from googleapiclient.errors import HttpError

with open('notion_credentials.json', 'r') as creds:
    notion_creds = json.load(creds)
with open('google_calendars.json', 'r') as calendars:
    google_calendars = json.load(calendars)['calendars']
with open('tag_filters.json', 'r') as filters:
    tag_filters = json.load(filters)['filters']

for i in range(2):
    print(i)
    data_notion = get_clean_data_from_notion(notion_creds['token'],
                                             notion_creds['database_id'])
    data_filtered = filter_by_tags(data_notion, tag_filters)

    data_filtered = filter_by_time(data_notion)

##    for i,event in enumerate(data_filtered):
##        try:
##            if is_event_new(event):
##                calendar_name = event['GoogleCalendar']
##                try:
##                    google_calendar_id = [x['id'] for x in google_calendars
##                                          if x['name'] == event['GoogleCalendar']][0]
##                except IndexError:
##                    google_calendar_id = 'primary'
##                event_id = create_event_google_calendar(calendar_id = google_calendar_id,
##                                                        summary = event['name'],
##                                                        description = event['description'],
##                                                        start = event['start'],
##                                                        end = event['end'])
##                event['google_id'] = event_id
##                save_event(event)
##        except HttpError:
##            print(f"Unfortunately, it was not possible to creat event {summary}.")
##            print()
##    time.sleep(1)
