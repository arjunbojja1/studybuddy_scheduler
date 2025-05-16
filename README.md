# StudyBuddy Scheduler

StudyBuddy Scheduler is a smart and interactive planner designed to help students create effective study schedules based on their availability, workload, and deadlines. It offers multiple scheduling strategies and integrates motivational quotes to keep users inspired while they work.

This project was developed as part of a class assignment for the University of Maryland's INST326 course. It demonstrates skills in Python programming, web development, API integration, and data visualization.

**Note**: As per the project instructions, the entire application was built using Python and Python-based libraries only.

---

## Features

- **User-Friendly Interface**: A browser-based UI built with ReactPy for seamless user interaction.
- **Customizable Scheduling**: Input courses, deadlines, estimated time commitments, and preferred study hours.
- **Multiple Scheduling Strategies**:
  - **Urgency-Based**: Prioritizes courses with earlier deadlines.
  - **Even Distribution**: Spreads study time evenly across available days.
  - **Pomodoro-Style**: Creates 25-minute work blocks with 5-minute breaks.
- **Downloadable Schedules**: Export study plans in CSV or plain text format.
- **Motivational Quotes**: Displays motivational quotes fetched from the ZenQuotes API.
- **Interactive Calendar View**: Visualize schedules in a calendar format with progress tracking.

---

## Technologies Used

- **Frontend**: ReactPy
- **Backend**: FastAPI
- **Data Visualization**: Matplotlib
- **API Integration**: ZenQuotes API
- **Testing**: Pytest

---

## How to Run the Program

Before you begin, ensure you have [Python](https://www.python.org/downloads/) installed.

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

### 5. **Access the app**
Open your browser and navigate to:
```bash
http://localhost:8000
```

---

## Learning Objectives

This project demonstrates the following skills:
- Building a full-stack application using Python.
- Designing and implementing a browser-based UI with ReactPy.
- Integrating third-party APIs for real-time data (ZenQuotes API).
- Implementing multiple scheduling algorithms.
- Writing unit tests to ensure code reliability.
- Visualizing data using Matplotlib.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

