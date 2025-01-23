from icalendar_handler import get_ical_content
from tasks_api_handler import initialize_task_list
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values

if __name__ == "__main__":
    load_dotenv()

    # get ical file from url in env
    # (events, assignments) = get_ical_content(os.getenv("CANVAS_ICAL_URL"))
    # for assignment in assignments:
    #     print(assignment["name"])
    #     print(assignment["date"])

    # authenticate with google tasks
    initialize_task_list()
    