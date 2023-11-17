"""
Creates a new configuration file named 'config.txt' if it doesn't exist.

Steps:
    - Opens 'config.txt' in write mode and writes the default configuration content.

Expected Inputs: None

Outputs:
    - Generates a new 'config.txt' file with default configuration content.
"""
def _create_config_file():
    # Create a new configuration file if it doesn't exist
    with open('config.txt', 'w') as configFile:
        configFile.write('# Configuration File\n\n')

"""
Saves the provided URL to the configuration file 'config.txt'.

Steps:
    - Attempts to open 'config.txt' in append mode.
    - If the file doesn't exist, creates a new 'config.txt' file and writes the URL.
    - If the file exists, checks for the existence of [URL] tag, updates or appends the URL accordingly.

Expected Inputs:
    - url: A string representing the URL to be saved in the configuration file.

Outputs:
    - Appends or updates [URL] tag with the provided URL in 'config.txt'.
"""
def save_url_to_config(url):
    # Save a URL to the configuration file
    try:
        configFile = open('config.txt', 'a+')
    except FileNotFoundError:
        _create_config_file()
        configFile = open('config.txt', 'a+')
    finally:
        configFile.seek(0)
        lines = configFile.readlines()
        url_tag_exists = any('[URL]' in line for line in lines)
        
        # If the [URL] tag doesn't exist, write it along with the URL
        if not url_tag_exists:
            configFile.write('[URL]\n')
            configFile.write(f'url = {url}\n\n')
        else:
            # If the [URL] tag exists, update the URL value
            configFile.seek(0)
            updated_lines = []
            for line in lines:
                if '[URL]' in line:
                    updated_lines.append(f'url = {url}\n')
                else:
                    updated_lines.append(line)
            
            configFile.truncate(0)
            configFile.writelines(updated_lines)
        configFile.close()

"""
Reads and retrieves the URL stored in the configuration file 'config.txt'.

Steps:
    - Attempts to open 'config.txt' in read mode.
    - Searches for the [URL] tag and extracts the stored URL.

Expected Inputs: None

Outputs:
    - Returns the URL stored in 'config.txt' or None if not found.
"""
def read_url_from_config():
    # Read the URL from the configuration file
    try:
        with open('config.txt', 'r') as configFile:
            lines = configFile.readlines()
            for index, line in enumerate(lines):
                if '[URL]' in line:
                    url_line = lines[index + 1]
                    url = url_line.split('=')[1].strip()
                    return url
            return None
    except FileNotFoundError:
        return None

"""
Saves the provided task list name to the configuration file 'config.txt'.

Steps:
    - Attempts to open 'config.txt' in append mode.
    - If the file doesn't exist, creates a new 'config.txt' file and writes the task list name.
    - If the file exists, checks for the existence of [TASK_LIST] tag, updates or appends the task list name accordingly.

Expected Inputs:
    - taskListName: A string representing the task list name to be saved in the configuration file.

Outputs:
    - Appends or updates [TASK_LIST] tag with the provided task list name in 'config.txt'.
"""
def save_task_list_name(taskListName):
    # Save a task list name to the configuration file
    try:
        configFile = open('config.txt', 'a+')
    except FileNotFoundError:
        _create_config_file()
        configFile = open('config.txt', 'a+')
    finally:
        configFile.seek(0)
        lines = configFile.readlines()
        task_list_tag_exists = any('[TASK_LIST]' in line for line in lines)
        
        # If the [TASK_LIST] tag doesn't exist, write it along with the task list name
        if not task_list_tag_exists:
            configFile.write('[TASK_LIST]\n')
            configFile.write(f'name = {taskListName}\n\n')
        else:
            # If the [TASK_LIST] tag exists, update the task list name
            configFile.seek(0)
            updated_lines = []
            for line in lines:
                if '[TASK_LIST]' in line:
                    updated_lines.append(f'name = {taskListName}\n')
                else:
                    updated_lines.append(line)
            
            configFile.truncate(0)
            configFile.writelines(updated_lines)
        configFile.close()

"""
Retrieves the task list name stored in the configuration file 'config.txt'.

Steps:
    - Attempts to open 'config.txt' in read mode.
    - Searches for the 'name' attribute under [TASK_LIST] tag and extracts the stored task list name.

Expected Inputs: None

Outputs:
    - Returns the task list name stored in 'config.txt' or None if not found.
"""
def get_task_list_name():
    # Get the saved task list name from the configuration file
    try:
        with open('config.txt', 'r') as configFile:
            lines = configFile.readlines()

        for line in lines:
            if "name" in line:
                taskListName = line.split("=")[1].strip()
                return taskListName
        return None
    except FileNotFoundError:
        return None
