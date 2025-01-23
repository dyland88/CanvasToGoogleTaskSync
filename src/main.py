import datetime
from cache_handler import *
from config_handler import *
from icalendar_handler import get_ical_content
from tasks_api_handler import *
import os
from dotenv import load_dotenv

def get_changed_assignments(assignments, file="assignments.txt"):
    previous_assignments = load_assignments_from_file()
    changed_assignments = []
    for assignment in assignments:
        for previous_assignment in previous_assignments:
            if(assignment["name"] == previous_assignment["name"]):
                if(assignment["date"] != previous_assignment["date"]):
                    print("Due date changed for assignment: " + assignment["name"])
                    changed_assignments.append(assignment)
                break
    return changed_assignments


if __name__ == "__main__":
    load_dotenv()

    # authenticate with google tasks
    initialize_task_list()
    set_task_list("Assignments")

    # get ical file from url in env
    assignments = get_ical_content(os.getenv("CANVAS_ICAL_URL"), 14)
    print("Retrieved calendar from Canvas")
    changed_assignments = get_changed_assignments(assignments)
    
    
                
    save_assignments_to_file(assignments)


    