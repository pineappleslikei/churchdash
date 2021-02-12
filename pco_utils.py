from datetime import datetime, timedelta
import fetch as f

today = datetime.now()
dash_display_name = 'Chris'


def pco_people_pipeline():
    service_type_ids = f.get_pco_service_types()
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


# def status_stats(pco_people):
#     status = {
#         'confirmed': 0,
#         'unconfirmed': 0,
#         'declined': 0
#     }
#     for plan in pco_people:
#         for person in plan['people']:
#             if person['status'] == 'C':
#                 status['confirmed'] += 1
#             if person['status'] == 'U':
#                 status['unconfirmed'] += 1
#             if person['status'] == 'D':
#                 status['declined'] += 1
#     return status

def status_stats(pco_people):
    status = []
    for plan in pco_people:
        for person in plan['people']:
            status.append(person['status'])
    return status


def is_it_this_week(plan_sort_date):
    if today + timedelta(days=7) < plan_sort_date:
        return False
    else:
        return True


pco_people = pco_people_pipeline()
people_stats = status_stats(pco_people)
