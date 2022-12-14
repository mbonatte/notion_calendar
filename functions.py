import os.path
import json
import datetime

def filter_by_tags(events, tags):
    data_filtered = []
    for event in events:
        for tag in tags:
            if all(elem in event['tag'] for elem in tag):
                data_filtered.append(event)
                break
    return data_filtered

def convert_to_datetime(time):
    try:
        event_date = datetime.datetime.strptime(time,
                                                '%Y-%m-%dT%H:%M:%S.%f0%z')
    except ValueError:
        pass
    try:
        event_date = datetime.datetime.strptime(time,
                                                '%Y-%m-%d')
    except ValueError:
        pass
    return event_date
    

def filter_by_time(events, time=datetime.date.today()):
    data_filtered = []
    for event in events:
        event_date = convert_to_datetime(event['start'])
        if time <= event_date.date():
            data_filtered.append(event)
    return data_filtered

def save_event(event, file_name=None):
    if file_name is None:
        file_name = 'events_saved.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            events = json.load(f)['events']
        events.append(event)
        with open(file_name, 'w') as f:
            json.dump({'events': events}, f, indent=4)
    else:
        with open(file_name, 'w') as f:
            json.dump({'events': [event]}, f, indent=4)

def update_event(event, file_name=None):
    if file_name is None:
        file_name = 'events_saved.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            events = json.load(f)['events']
        for i,e in enumerate(events):
            if event['notion_id'] == e['notion_id']:
                events[i] = event
        with open(file_name, 'w') as f:
            json.dump({'events': events}, f, indent=4)
    else:
        with open(file_name, 'w') as f:
            json.dump({'events': [event]}, f, indent=4)

def is_event_new(event):
    if os.path.exists('events_saved.json'):
        with open('events_saved.json', 'r') as f:
            events = json.load(f)['events']
            for e in events:
                if event['notion_id'] == e['notion_id']:
                    return False
    return True

def is_event_modified(event):
    if os.path.exists('events_saved.json'):
        with open('events_saved.json', 'r') as f:
            events = json.load(f)['events']
            for e in events:
                if event['notion_id'] == e['notion_id']:
                    if (convert_to_datetime(event['last_edited_time'])
                        >
                        convert_to_datetime(e['last_edited_time'])):
                        return True
    return False
