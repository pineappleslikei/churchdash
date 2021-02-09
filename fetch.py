import requests
import json
import pickle
import os.path
import pco_credentials as p_cred
import pco_config as p_conf
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
    results = service.users().messages().list(userId='me').execute()
    # placeholder return. need to figure out grabbing subject lines. only returns thread ids right now
    return results.get('messages', [])


def get_pco_service_types():
    response = requests.get(
        f'{p_conf.BASE_URL}/service_types', auth=(p_cred.app_id, p_cred.secret)).json()
    service_ids = [service['id'] for service in response['data']]
    return service_ids


def get_pco_plans(service_id):
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}/{service_id}/plans', auth=(p_cred.app_id, p_cred.secret), params={'filter': 'future'}).json()
    if len(response['data']) > 0:
        plan_ids = {'service_type': service_id, 'plans': [
            plan['id'] for plan in response['data']]}
        return plan_ids
    else:
        return None


def get_pco_plan_people(service_id, plan_id):
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}/{service_id}/plans/{plan_id}/team_members', auth=(p_cred.app_id, p_cred.secret), params={'include': 'plan'}).json()
    try:
        plan_date = response['included'][0]['attributes']['dates']
        sort_date = response['included'][0]['attributes']['sort_date']
        plan = {'pretty_date': plan_date, 'people': [], 'sort_date': sort_date}
        for person in response['data']:
            plan['people'].append(
                {'name': person['attributes']['name'],
                 'status': person['attributes']['status'],
                 'position': person['attributes']['team_position_name']})
        return plan
    except IndexError:
        return False


def get_songs():
    pass
