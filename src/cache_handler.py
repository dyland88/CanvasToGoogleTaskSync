import datetime


def save_assignments_to_file(assignments, filename="assignments.txt"):
        with open(filename, "w") as file:
            for assignment in assignments:
                file.write(f"{assignment['name']}\n{assignment['date']}\n")


"""
returns object with name and date of previous assignments
name: string
date: date
"""
def load_assignments_from_file(filename="assignments.txt"):
    assignments = []
    with open(filename, "r") as file:
        while True:
            name = file.readline().strip()
            if not name:
                break
            date_string = file.readline().strip()
            date_format = "%Y-%m-%d"
            date = datetime.datetime.strptime(date_string, date_format).date()
            assignments.append({"name": name, "date": date})
    return assignments

"""
Returns array of assignments whose due date is changed from the date stored in file.
"""
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

"""
returns array of assignments that were not in the previous update
"""
def get_new_assignments(assignments, file="assignments.txt"):
    previous_assignments = load_assignments_from_file()
    new_assignments = []
    previous_assignment_names = {assignment["name"] for assignment in previous_assignments}
    for assignment in assignments:
        if assignment["name"] not in previous_assignment_names:
            print("New assignment found: " + assignment["name"])
            new_assignments.append(assignment)
    return new_assignments