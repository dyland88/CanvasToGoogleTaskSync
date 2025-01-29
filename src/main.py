import datetime
from cache_handler import *
from config_handler import *
from icalendar_handler import get_ical_content
from tasks_api_handler import *
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    # authenticate with google tasks
    initialize_task_list()
    set_task_list("Assignments")

    # get ical file from url in env
    assignments = get_ical_content(os.getenv("CANVAS_ICAL_URL"), 2)
    print("Retrieved calendar from Canvas")
    changed_assignments = get_changed_assignments(assignments)
    new_assignments = get_new_assignments(assignments)
    print(get_current_tasks())


    
    for assignment in new_assignments:
        create_task(assignment["name"], "", assignment["date"])
    
    
    save_assignments_to_file(assignments)


    