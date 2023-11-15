import requests
import icalendar

"""
    [Internal] Fetches an iCalendar file from a given URL.

    Args:
        url (str): The URL pointing to the iCalendar file.

    Returns:
        str: The text content of the fetched iCalendar file.

    Raises:
        Exception: If fetching the iCalendar file fails due to a non-200 status code.
"""
def _fetch_ical_from_web(url):
    # Fetch iCalendar file from the web using the provided URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.text
    else:
        # Raise an exception if fetching the iCalendar file failed
        raise Exception(f"Failed to fetch iCalendar file. Status code: {response.status_code}")

"""
    Fetches and parses iCalendar content from the provided URL.

    Args:
        URL (str): The URL pointing to the iCalendar file (taken from the Canvas calendar page).

    Returns:
        tuple: A tuple containing two lists - events and assignments.
               events (list): List of regular events with start dates.
               assignments (list): List of assignments.

    Raises:
        Exception: If there's an error fetching or parsing the iCalendar content.
"""
def get_ical_content(URL):
    try:
        ical_content = _fetch_ical_from_web(URL)
    except Exception as e:
        print(f"Error fetching iCal content: {e}")
        raise

    # Parse the fetched iCalendar content
    cal = icalendar.Calendar.from_ical(ical_content)
    events = []
    assignments = []
    
    # Iterate through each component in the iCalendar data
    for component in cal.walk():
        if component.name == "VEVENT":
            # Check if the component is an assignment (missing start or end date)
            is_assignment = 'dtstart' not in component or 'dtend' not in component
            event = {
                "name": component.get('summary'),
                "date": component.get('dtstart').dt,
                "description": component.get('description'),
                "is_assignment": is_assignment,
            }
            # Categorize events as assignments or regular events
            if event["is_assignment"]:
                assignments.append(event)
            else:
                events.append(event)
    
    return events, assignments