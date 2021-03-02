import requests
import json
import pco_credentials as p_cred
import pco_config as p_conf
import date_utils as d


def get_pco_service_types():
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}',
        auth=(p_cred.app_id, p_cred.secret)
    ).json()
    service_ids = [service['id'] for service in response['data']]
    return service_ids


def get_pco_plans(service_id):
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}/{service_id}/plans',
        auth=(p_cred.app_id, p_cred.secret),
        params={'filter': 'future'}
    ).json()
    if len(response['data']) > 0:
        plan_ids = {'service_type': service_id, 'plans': [
            plan['id'] for plan in response['data']]}
        return plan_ids
    else:
        return None


def get_past_pco_plans(service_id):
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}/{service_id}/plans',
        auth=(p_cred.app_id, p_cred.secret),
        params={
            'filter': 'past',
            'per-page': '8',
            'order': '-sort_date'
        }
    ).json()
    past_plan_ids = [plan['id'] for plan in response['data']
                     if d.was_it_recent(plan['attributes']['sort_date'])]
    return past_plan_ids


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


def get_plan_items(service_type_id, plan_id):
    response = requests.get(
        f'{p_conf.BASE_URL}{p_conf.types_ep}/{service_type_id}/plans/{plan_id}/items',
        auth=(p_cred.app_id, p_cred.secret),
        params={'include': 'song'}
    ).json()
    plan_songs = [song['attributes']['title'] for song in response['included']]
    return plan_songs
