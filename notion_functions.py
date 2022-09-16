import requests
import json

def get_raw_data_from_notion(token, database_id):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", url, headers=headers)
    data = res.json()
    return data


def get_clean_data_from_notion(token, database_id):
    data_notion = get_raw_data_from_notion(token, database_id)
    with open('notion_data.json', 'w') as outfile:
        json.dump(data_notion, outfile)
    data_clean = []
    for item in data_notion['results']:
        try:
            event = {'notion_id': item['id'],
                     'name': item['properties']['Name']['title'][0]['text']['content'],
                     'start': item['properties']['Date']['date']['start'],
                     'end': item['properties']['Date']['date']['end'],
                     'url': item['properties']['URL']['url'],
                     'description': '',
                     }
        except IndexError:
            break
        try:
            event['GoogleCalendar'] = item['properties']['GoogleCalendar']['select']['name']
        except TypeError:
            event['GoogleCalendar'] = 'primary'
        try:
            event['description'] = item['properties']['Text']['rich_text'][0]['text']['content']
        except IndexError:
            event['description'] = ''
        event['tag'] = []
        for i,tag in enumerate(item['properties']['Tags']['multi_select']):
            event['tag'].append(tag['name'])
        data_clean.append(event)
    return data_clean
