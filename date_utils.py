from datetime import datetime, timedelta

today = datetime.now()


def is_it_this_week(plan_sort_date):
    sort_dt_obj = datetime.strptime(plan_sort_date[:10], '%Y-%m-%d')
    if today + timedelta(days=14) < sort_dt_obj:
        return False
    else:
        return True


def was_it_recent(plan_sort_date):
    sort_dt_obj = datetime.strptime(plan_sort_date[:10], '%Y-%m-%d')
    if today - timedelta(days=90) > sort_dt_obj:
        return False
    else:
        return True
