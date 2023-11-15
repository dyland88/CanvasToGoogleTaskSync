# Canvas to Google Tasks Sync
This project aims to automate the synchronization of academic assignments and events from Canvas LMS to Google Tasks for efficient task management.

## Description

The Canvas to Google Tasks Sync is a Python-based tool that utilizes Canvas LMS iCalendar features and Google Tasks API to retrieve academic assignments from Canvas and add them as tasks to Google Tasks.

## Features

- ✅ Canvas Integration (using iCalendar)
- ✅ Google Tasks API Integration
- ❌ User-Controlled Selective Canvas Calendar Sync (WIP)
- ❌ Task Deduplication with Hashing
- ❌ Cloud Hosting for Automated Sync
- ❌ Intuitive UI for Sync Setup

## Requirements

To run this script, ensure you have the necessary Python packages installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the Repository:
```bash
git clone https://github.com/jisaiaha/CanvasToGoogleTaskSync.git
cd CanvasToGoogleTaskSync
```
2. Create a Virtual Environment:
```bash
# Create a virtual environment (replace 'myenv' with your preferred name)
python -m venv myenv  # Windows
python3 -m venv myenv  # macOS/Linux
```

3. Activate the Virtual Environment:
```bash
# Activate the virtual environment
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate     # Windows
```

4. Install Required Packages:
```bash
# Execute your application or scripts
python your_main_script.py
```

5. Run main.py
```bash
# Execute your application or scripts
python main.py
```

6. Deactivate the Virtual Environment
```bash
# When finished, deactivate the virtual environment
deactivate
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository, make your changes, and create a pull request.