from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
# from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    # Getting lists of data and its respective fields
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])  # Getting the files metadata based on the file id from the function above

    # Listing out the files
    if not items:
        print('No files found.')
    else:
        print('Files:')
        i = 0
        for item in items:
            print('{0} {1}'.format(i, item['name']))
            i += 1

    # Using a while loop in case of any errors due to insufficient permission
    while True:
        try:
            print("")
            index = int(input("Enter the number of the file you want to check: "))
            print("")

            # Getting list of revision of a file by its file id
            resultrev = service.revisions().list(
                fileId=items[index]["id"], fields="revisions(id, modifiedTime, lastModifyingUser)").execute()

            break
        except:  # Using Except to count in any type of errors
            print("Oops! There was an error, please try another index")

    # Getting the content of the revision based on the file id and revision id from the function above
    itemsrev = resultrev.get('revisions', [])

    print("Users that made contributes to the file: ")
    for items in itemsrev:
        print(items['lastModifyingUser']['displayName'])


if __name__ == '__main__':
    main()