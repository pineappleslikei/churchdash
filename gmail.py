import base64
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def google_auth_flow():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_gmail():
    creds = google_auth_flow()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(
        userId='me',
        q='from:cellis@moochurch.org subject:todo'
    ).execute()
    raw_todo_items = []
    for message in results['messages']:
        item = service.users().messages().get(
            userId='me', id=message['id'], format='full').execute()
        raw_message = item['payload']['parts'][0]['body']['data']
        raw_todo_items.append(
            str(base64.urlsafe_b64decode(raw_message), 'utf-8'))
    todo_items = [gmail_body_parser(item) for item in raw_todo_items]
    return todo_items


def gmail_body_parser(message_body):
    garbage = [
        '6289', '*Chris Ellis**Student Worship Arts Director**Mount of Olives Church*cellis@moochurch.orgcall/text (949) 306', '']
    raw_list = message_body.split('-')
    clean_list = []
    for item in raw_list:
        clean_item = item.replace('\r\n', '')
        if clean_item not in garbage:
            clean_list.append(clean_item)
    return clean_list
