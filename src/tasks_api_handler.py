# Import necessary modules and libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from threading import Lock
import pickle
import os

# Define global constants
SCOPES = ['https://www.googleapis.com/auth/tasks']
CHAR_LIMIT = 8000

# Define global variables
CREDS = None
SERVICE = None
TASKLISTID = None

"""
Initializes the Google Tasks API by obtaining credentials and creating a service instance.

This function aims to set up the Google Tasks API service by fetching necessary credentials
and constructing a service object to interact with the Tasks API. It involves the following steps:

- Obtains credentials using the '_get_credentials()' function.
- Builds the service using the obtained credentials with the 'build()' method.
- If successful, assigns the obtained credentials and service instance to global variables
    'CREDS' and 'SERVICE', respectively.
- Prints a success message indicating successful initialization of the Google Tasks API.

Expected Conditions:
- The '_get_credentials()' function should return valid credentials.
- The 'build()' method should successfully create a service instance for the Tasks API.

Outputs:
- If successful, assigns the obtained credentials to the global variable 'CREDS'.
- If successful, assigns the created service instance to the global variable 'SERVICE'.
- Prints a success message upon successful initialization.

Raises:
- Any exceptions raised during the initialization process are caught and re-raised to 
    provide information on the encountered error.
"""
def initialize_task_list():
    global CREDS, SERVICE
    try:
        CREDS = _get_credentials()
        SERVICE = build('tasks', 'v1', credentials=CREDS)
        print("Google Tasks API initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing Google Tasks API: {e}")
        raise

"""
Sets the global variable TASKLISTID to the ID of the specified task list.

This function aims to set the global variable TASKLISTID to the ID of the task list
identified by the provided 'taskListName'. The function involves the following steps:

- Calls the '_get_task_list_id()' function to retrieve the ID of the specified task list.
- If successful, assigns the obtained task list ID to the global variable 'TASKLISTID'.

Args:
- taskListName (str): The name of the task list to be set.

Expected Conditions:
- The '_get_task_list_id()' function should successfully find the ID for the specified task list.

Outputs:
- If successful, assigns the obtained task list ID to the global variable 'TASKLISTID'.

Raises:
- Raises a ValueError if the specified task list name is not found or does not exist.
"""
def set_task_list(taskListName):
    global TASKLISTID
    try:
        TASKLISTID = _get_task_list_id(taskListName)
    except ValueError as e:
        raise

"""
Creates a task in the Google Tasks service with the provided information.

This function aims to create a task in the Google Tasks service by utilizing the
authorized credentials and the global variable TASKLISTID as the target task list.
The function involves the following steps:

- Validates if the TASKLISTID has been set. Raises a RuntimeError if TASKLISTID is None.
- Prepares the task data using the provided title, notes, and due_date.
- Attempts to create the task using the Google Tasks API 'insert' method.

Args:
- title (str): The title or name of the task.
- notes (str): Additional notes or description for the task.
- due_date (datetime): The due date for the task.

Expected Conditions:
- TASKLISTID should be set and authorized credentials available for the Google Tasks service.

Outputs:
- Returns the created task if successful.

Raises:
- Raises a RuntimeError if the TASKLISTID is not set before performing this operation.
- Handles HTTP errors (HttpError) if encountered during task creation.
- Raises an Exception if an unexpected error occurs while creating the task.
"""
# Create a task in the specified task list
def create_task(title, notes, due_date):
    if TASKLISTID is None:
        raise RuntimeError("Task list ID is not set. Please set the task list ID before performing this operation.")
    
    # Prepare task data
    task = {
        'title': title,
        'notes':    None if notes is None 
                    else _truncateString(notes) if len(notes) > CHAR_LIMIT
                    else notes,
        'due': _formatDateString(due_date) if due_date else None,
    }
    
    # Attempt to create the task
    try:
        return SERVICE.tasks().insert(tasklist=TASKLISTID, body=task).execute()
    except HttpError as e:
        print(f"HTTP error occurred: {e}")
        raise
    except Exception as error:
        print(f"An unexpected error occurred while creating the task: {error}")
        raise

"""
Clears all tasks from the specified task list in the Google Tasks service.

This function is designed to clear all tasks from the specified task list using the global variable
TASKLISTID as the target task list. The function involves the following steps:

- Validates if the TASKLISTID has been set. Raises a RuntimeError if TASKLISTID is None.
- Initializes a lock and a set to track ongoing deletions for synchronization among deletion threads.
- Retrieves the tasks in the specified task list using the Google Tasks API 'list' method.
- Processes tasks by deleting them iteratively using the 'delete' method for each task.
- Uses a lock to prevent concurrent deletion of the same task ID, allowing only one thread to delete a task ID at a time.
- Asserts that all tasks have been cleared from the task list. Raises AssertionError if some tasks remain.

Expected Conditions:
- TASKLISTID should be set to the desired task list before executing this operation.

Raises:
- Raises a RuntimeError if the TASKLISTID is not set before performing this operation.
- Handles HTTP errors (HttpError) if encountered during task list retrieval.
- Raises AssertionError if some tasks remain after attempted deletion.
"""
def clear_task_list():
    if TASKLISTID is None:
        raise RuntimeError("Task list ID is not set. Please set the task list ID before performing this operation.")
    
    # Initialize a lock and a set to track ongoing deletions
    deletion_lock = Lock()
    ongoing_deletions = set()
    
    # Retrieve tasks in the task list
    try:
        tasks = SERVICE.tasks().list(tasklist=TASKLISTID).execute()
    except HttpError as e:
        if e.resp.status == 404:
            print("Task list not found.")
            raise
        else:
            # Handle other HTTP errors if necessary
            print(f"An HTTP error occurred: {e}")
            raise
    
    # Process tasks if the task list is found
    while tasks.get('items'):
        for task in tasks.get('items', []):
            task_id = task['id']

            # Acquire the lock before processing the task
            deletion_lock.acquire()

            # Check if the task ID is already in ongoing deletions
            if task_id not in ongoing_deletions:
                # Add the task ID to ongoing deletions to lock it
                ongoing_deletions.add(task_id)
                
                # Release the lock before making the delete request
                deletion_lock.release()
                
                # Make the delete request
                try:
                    SERVICE.tasks().delete(tasklist=TASKLISTID, task=task_id).execute()
                except HttpError as e:
                    print(f"HTTP error occurred while deleting task {task_id}: {e}")      

                # Remove the task ID from ongoing deletions after deletion is complete
                deletion_lock.acquire()
                ongoing_deletions.remove(task_id)
                deletion_lock.release()

        try:
            tasks = SERVICE.tasks().list(tasklist=TASKLISTID).execute()
        except HttpError as e:
            if e.resp.status == 404:
                print("Task list not found.")
                raise
            else:
                # Handle other HTTP errors if necessary
                print(f"An HTTP error occurred: {e}")
                raise

    # Ensure all tasks are cleared
    assert not tasks.get('items'), f"Failed to clear all tasks in the list (ID: {TASKLISTID}). Some tasks remain."

"""
Retrieves and manages Google API credentials.

This function is responsible for managing Google API credentials for the application.
It involves the following steps:

- Checks if a credentials file named 'token.pickle' exists.
- Loads the credentials from the file if it exists.
- If no valid credentials are available or the existing credentials are not valid,
    it requests fresh credentials from the user using OAuth.
- Saves the obtained credentials to the 'token.pickle' file for subsequent use.
- Returns the obtained or newly refreshed credentials.

Returns:
- Credentials: Google API credentials necessary for making API calls.

Raises:
- Error handling for potential exceptions such as FileNotFoundError when the credentials file is not found,
    and other exceptions that might occur during the credential retrieval process.
"""
def _get_credentials():
    credentials = None

    # Check if credentials file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If no valid credentials are available, request them from the user
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return credentials

"""
Retrieves the ID of a task list given its name.

This function calls the Google Tasks API to obtain a list of task lists.
It then searches for a task list with the specified name.
If the task list is found, it returns its unique ID; otherwise, it raises a ValueError.

Args:
- taskListName (str): The name of the task list to search for.

Returns:
- str: The ID of the task list if found.

Raises:
- ValueError: If the task list with the provided name is not found.
"""
def _get_task_list_id(taskListName):
    # Call the Google Tasks API to get the task lists
    results = SERVICE.tasklists().list().execute()

    # Search for the task list with the specified name
    for tl in results.get('items', []):
        # print(f"Task list found: {tl['title']}")
        if tl['title'] == taskListName:
            task_list = tl
            break
    else:
        task_list = None

    # If the task list is not found, raise a ValueError
    if not task_list:
        raise ValueError(f"Task list with the name '{taskListName}' not found.")
    else:
        # Return the ID of the task list if found
        print("Selected list: " + task_list['title'])
        return task_list['id']
    

"""
Returns an array containing the names of the task lists
"""
def get_task_lists():
    # Call the Google Tasks API to get the task lists
    results = SERVICE.tasklists().list().execute()
    task_lists = []

    # Search for the task list with the specified name
    for tl in results.get('items', []):
        task_lists.append(tl['title'])

    return task_lists

"""
Formats a date string to RFC3339 format.

This function takes in a date and returns it in RFC3339 format, which is required
for specific Google Tasks API operations.

Args:
- d (datetime): The date object to be formatted.

Returns:
- str: The formatted date string in RFC3339 format.
"""
def _formatDateString(d):
    return ('%04d-%02d-%02dT00:00:00-04:00' %
            (d.year, d.month, d.day,)) 

"""
Truncates a string to a specified limit.

This function truncates the input string to the given character limit.
If the input string exceeds the limit, it is shortened and a message indicating
the character limit is appended.

Args:
- input_string (str): The string to be truncated.
- limit (int, optional): The character limit (default is 8000).

Returns:
- str: The truncated string with a message if the limit was reached.
"""
def _truncateString(input_string, limit=8000):
    truncated_string = input_string[:limit]
    return truncated_string + "\n\n Character limit reached"