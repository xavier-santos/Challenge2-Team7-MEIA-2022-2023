import json
from Models.week import Week

# Exports week as json file
# Format:
# {
#  "week_plan": [
#   {"day": "day_name",
#    "workers_schedule":[
#      {
#        "worker_id": worker_id,
#        "start_time": start_time,
#        "end_time": end_time,
#        "assigned_engines":[
#          {
#            "engine_id": engine_id,
#            "maintenance_time": maintenance_time,
#            "start_time": start_time,
#            "end_time": end_time
#          },
#        ]
#      },
#    ]
#   },
#  ]
# }
#

# Definition of the dictionary of weekdays
week_days_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def export_week(week: Week, file_name: str):
    week_plan = []
    for i in range(7):
        day = {"day": week_days_dict[i], "workers_schedule": []}
        for worker_week in week.workers_weeks_list:
            worker_schedule = {"worker_id": worker_week.worker.worker_id, "start_time": worker_week.worker.start_time,
                               "end_time": worker_week.worker.end_time, "assigned_engines": []}
            assigned_engines = worker_week.day_list[i].assigned_engine_list
            assigned_hours = 0
            flag = True
            for engine in assigned_engines:
                assigned_engine = {"engine_id": engine.engine_id, "maintenance_time": engine.maintenance_time,
                                   "start_time": worker_week.worker.start_time + assigned_hours, "end_time": worker_week.worker.start_time + assigned_hours+engine.maintenance_time}
                worker_schedule["assigned_engines"].append(assigned_engine)
                assigned_hours += engine.maintenance_time
                if (assigned_hours >= (worker_week.worker.end_time - worker_week.worker.start_time)/2) & flag:
                    assigned_hours += 1
                    flag = False
            day["workers_schedule"].append(worker_schedule)
        week_plan.append(day)
    with open(file_name, 'w') as outfile:
        json.dump({"week_plan": week_plan}, outfile, indent=2)
