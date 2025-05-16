# Manual Testing Guide - StudyBuddy Scheduler

This document outlines how to test the core features of the StudyBuddy Scheduler application.

## 1. Launch the App

### Steps:
1. Navigate to the project root directory.
2. Run the app using:
```bash
python app.py
```
3. Open your browser and go to:
```bash
http://localhost:8000
```

## 2. Test Input Validation

### Steps:
1. Try submitting the form with empty fields. Ensure the app displays an error message like "Please fill in all fields."
2. Enter invalid data (e.g., negative hours or invalid dates) and verify that the app handles these cases gracefully.

## 3. Test Scheduling Strategies

### Steps:
1. Enter multiple courses with varying deadlines and hours.
2. Select each scheduling strategy (Even Distribution, Urgency-Based, Pomodoro) and generate a schedule.
3. Verify that:
   - "Even Distribution" spreads study time evenly across available days.
   - "Urgency-Based" prioritizes courses with earlier deadlines.
   - "Pomodoro" creates 25-minute study blocks with 5-minute breaks.

## 4. Test Export Functionality

### Steps:
1. Generate a schedule and click "Export to CSV." Verify that the downloaded file contains the correct schedule data in CSV format.
2. Click "Export to TXT" and ensure the downloaded file contains the correct schedule data in plain text format.

## 5. Test Motivational Quotes

### Steps:
1. Generate a schedule and verify that a motivational quote is displayed below the schedule.
2. Ensure the quote is in the format: "Quote - Author."

## 6. Test Calendar View

### Steps:
1. Generate a schedule and verify that the calendar view displays the schedule correctly.
2. Expand and collapse days to ensure the toggle functionality works as expected.
3. Mark tasks as complete and verify that the progress bar updates accordingly.