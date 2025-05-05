# StudyBuddy Scheduler

StudyBuddy Scheduler is a smart and interactive planner that helps students create study schedules based on their availability, workload, and deadlines. 
It offers several scheduling options and displays motivational quotes utilizing the ZenQuotes API to keep users inspired while they work.

StudyBuddy Scheduler is built in Python and provides a web based interface using ReactPy and runs from the command line.

StudyBuddy Scheduler was created by Arjun Bojja and Ryan Flynn.

---

## Features

- Collects user input through a browser based UI built with ReactPy
- Allows input of courses, deadlines, estimated time commitments, and preferred study hours
- Offers three scheduling strategies:
    - Urgency based
    - Evenly distributed
    - Pomodoro-style (25 minute work blocks and 5 minute break blocks)
- Generates a structured, downloadable study plan (CSV or text)
- Integrates the ZenQuotes API to display a quotes with each schedule
- Written in Python and runs in the command line

---

## How to Run the Program
Before you begin, make sure you have [Python](https://www.python.org/downloads/) installed.

### 1. **Create a virtual environment**
```bash
python -m venv venv
```
If this does not work, execute the following:
```bash
python3 -m venv venv
```
### 2. **Activate your virtual environment**
#### macOS
```bash
source venv/bin/activate
```
#### Windows
```bash
venv\Scripts\activate
```
### 3. **Install the required dependencies**
```bash
pip install -r requirements.txt
```
### 4. **Run the app**
```bash
python app.py
```

