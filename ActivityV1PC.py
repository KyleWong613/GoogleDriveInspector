from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import operator
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/activity'

def main():
    """Shows basic usage of the Drive Activity API.
    Prints information about the last 10 events that occured the user's Drive.
    """
    store = file.Storage('tokenforactivity.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('appsactivity', 'v1', http=creds.authorize(Http()))

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com',
        drive_ancestorId='root',pageSize=10).execute()
    activities = results.get('activities', [])

    if not activities:
        print('No activity.')
    else:
        print('Recent activity:')
        x = "application/vnd.google-apps.document"
        dict = {}
        counter = 1
        dataarray = []
        for activity in activities:
            type = activity['combinedEvent'].get('target',None)['mimeType']
            name = activity['combinedEvent'].get('target',None)['id']

            #ID CAN BE INCORPORATED TO CATER USER INPUT
            id = '16vybA6bmemoHO1CQvH3cukq7K9rIoQuNXtZSqicCLAc'
            
            if type == x and id == name:
                event = activity['combinedEvent']
                user = event.get('user', None)
                target = event.get('target', None)
                if user is None or target is None:
                    continue
                timer = datetime.datetime.fromtimestamp(
                    int(event['eventTimeMillis'])/1000)
                dataarray.append([counter, user['name'], event['primaryEventType'], timer])
                '''if user['name'] in dict:
                    dataarray.append([counter,user['name'],event['primaryEventType'],timer])
                    #dict.update({counter:{'name':user['name'],'type': event['primaryEventType'],'time': timer}})
                else:

                    #dict.update({counter:{'name':user['name'],'type': event['primaryEventType'],'time': timer}})
                '''
                print('{0}: {1}, {2}, {3} ({4})'.format(timer, user['name'],
                    event['primaryEventType'], target['name'], target['mimeType']))
                counter+=1
            else:
                pass
        '''for item, item2 in dict.items():
            print('{0} {1} {2}'.format(item2['name'], item2['type'], item2['time']))'''
        print()
        print("sort by user")
        print()

        dataarray.sort(key = lambda x: x[1]) #sort based on name
        for i in dataarray:
            print(i)
        print("sort by changes")
        print()
        dataarray.sort(key = lambda x: x[2]) #sort based on changes type
        for i in dataarray:
            print(i)
        '''for item, item2 in dict.items():
            
            print('{0} {1} {2}'.format(item2['name'], item2['type'], item2['time']))'''



if __name__ == '__main__':
    main()