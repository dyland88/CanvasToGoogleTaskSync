import datetime
from cache_handler import *
from config_handler import *
from icalendar_handler import get_ical_content
from tasks_api_handler import *
import os
from dotenv import load_dotenv

def find_new_and_updated_assignments(assignments, current_tasks):
    new_assignments = []
    updated_assignments = []

    # Create a dictionary of current tasks for quick lookup
    task_dict = {task['title']: task for task in current_tasks}

    for assignment in assignments:
        assignment_name = assignment['name']
        assignment_due_date = assignment['date']

        if assignment_name not in task_dict:
            # Assignment not found in current tasks, it's a new assignment
            new_assignments.append(assignment)
        else:
            # Assignment found, check if the due date has changed
            task_due_date = task_dict[assignment_name].get('due')
            if task_due_date:
                task_due_date = datetime.datetime.strptime(task_due_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                if task_due_date != assignment_due_date:
                    updated_assignments.append((task_dict[assignment_name]['id'], assignment_due_date))

    return new_assignments, updated_assignments

if __name__ == "__main__":
    load_dotenv()

    # Authenticate with Google Tasks
    initialize_task_list()
    set_task_list("School")

    # Get iCal file from URL in env
    assignments = get_ical_content(os.getenv("CANVAS_ICAL_URL"), 21)
    print("Retrieved calendar from Canvas")
    # assignments[0]["date"] = assignments[5]["date"]   
    
    # current_tasks = get_current_tasks()
    current_tasks = get_all_tasks()

    # Find new and updated assignments
    new_assignments, updated_assignments = find_new_and_updated_assignments(assignments, current_tasks)

    # Print new and updated assignments
    print("New Assignments:")
    for assignment in new_assignments:
        print(assignment['name'])
        # Create new task in Google Tasks
        # create_task(assignment['name'], assignment.get('description', ''), assignment['date'])
        create_task(assignment['name'], "", assignment['date'])

    print("\nUpdated Assignments:")
    for task_id, new_due_date in updated_assignments:
        print(f"Task ID: {task_id}, New Due Date: {new_due_date}")
        # Update the due date of the existing task in Google Tasks
        update_task_due_date(task_id, new_due_date)


    