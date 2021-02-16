from datetime import datetime, timedelta
import fetch as f

today = datetime.now()
service_ids = []


def pco_people_pipeline():
    service_type_ids = f.get_pco_service_types()
    service_ids.extend(service_type_ids)
    plan_ids = [f.get_pco_plans(service_id) for service_id in service_type_ids]
    upcoming_plans = []
    for item in plan_ids:
        if item != None:
            service_id = item['service_type']
            for plan in item['plans']:
                people = f.get_pco_plan_people(service_id, plan)
                if people:
                    upcoming_plans.append(people)
    return upcoming_plans


def pco_songs_pipeline():
    songs_used = []
    for service_id in service_ids:
        plan_ids = f.get_past_pco_plans(service_id)
        for plan in plan_ids:
            songs_used.extend(f.get_plan_items(service_id, plan))
    return songs_used


def status_stats(pco_people):
    status = []
    for plan in pco_people:
        for person in plan['people']:
            status.append(person['status'])
    return status


def date_sort_pipeline(pco_people):
    this_week_plans = []
    for plan in pco_people:
        if is_it_this_week(plan['sort_date']):
            this_week_plans.append(plan)
    return this_week_plans


def is_it_this_week(plan_sort_date):
    sort_dt_obj = datetime.strptime(plan_sort_date[:10], '%Y-%m-%d')
    if today + timedelta(days=14) < sort_dt_obj:
        return False
    else:
        return True


pco_people = pco_people_pipeline()
two_weeks_plans = date_sort_pipeline(pco_people)
people_stats = status_stats(two_weeks_plans)
two_weeks_sorted = sorted(two_weeks_plans, key=lambda plan: plan['sort_date'])
songs = pco_songs_pipeline()
