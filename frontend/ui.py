"""Frontend UI for the StudyBuddy Scheduler.

This script defines the ReactPy components for the StudyBuddy Scheduler
application. It includes the main UI for inputting courses, generating
schedules, and displaying results.
"""

from reactpy import component, html, use_state, event
from collections import defaultdict
from datetime import datetime
import random
import json
import urllib.parse

from exporter.file_exporter import FileExporter
from scheduler.scheduler_engine import SchedulerEngine
from scheduler.utils import generate_pie_chart
from api.quotes import QuoteFetcher


def radial_gradient(hovered):
    """Generates a radial gradient based on hover state.

    Args:
        hovered (bool): Whether the element is hovered.

    Returns:
        str: CSS gradient string.
    """
    if hovered:
        return "radial-gradient(circle at center, #e0f7fa, #c3e6cb, #f0f4f8)"
    else:
        return "radial-gradient(circle at top left, #f0f4f8, #e4eaf1)"
            
@component
def StudyBuddyUI():
    """Main UI component for the StudyBuddy Scheduler.

    Allows users to input courses, deadlines, and hours, select a scheduling
    strategy, and generate a study schedule. Users can also export the schedule
    and view motivational quotes.
    """
    course_entries, set_course_entries = use_state([
        {"course": "", "deadline": "", "hours": ""}
    ])
    generated_schedule, set_generated_schedule = use_state([])
    strategy, set_strategy = use_state("even")
    result, set_result = use_state("")
    quote, set_quote = use_state("")
    hovered, set_hovered = use_state(False)
    bg_hovered, set_bg_hovered = use_state(False)
    show_modal, set_show_modal = use_state(False)
    pending_delete_index, set_pending_delete_index = use_state(None)

    def add_course_entry():
        """Adds a new empty course entry."""
        set_course_entries(course_entries + [{"course": "", "deadline": "", "hours": ""}])

    def update_course_field(index, field, value):
        """Updates a specific field in a course entry.

        Args:
            index (int): Index of the course entry.
            field (str): Field to update ('course', 'deadline', or 'hours').
            value (str): New value for the field.
        """
        updated = course_entries[:]
        updated[index][field] = value
        set_course_entries(updated)

    def ask_to_delete(index):
        """Prompts the user to confirm deletion of a course entry.

        Args:
            index (int): Index of the course entry to delete.
        """
        set_pending_delete_index(index)
        set_show_modal(True)

    def confirm_delete():
        """Deletes the selected course entry after confirmation."""
        if pending_delete_index is not None and len(course_entries) > 1:
            updated = course_entries[:pending_delete_index] + course_entries[pending_delete_index + 1:]
            set_course_entries(updated)
        set_pending_delete_index(None)
        set_show_modal(False)

    def cancel_delete():
        """Cancels the deletion of a course entry."""
        set_pending_delete_index(None)
        set_show_modal(False)
        
    def get_download_link(filetype):
        """Generates a download link for the schedule.

        Args:
            filetype (str): File type ('csv' or 'txt').

        Returns:
            str: Download link.
        """
        if not generated_schedule or len(generated_schedule) == 0:
            return "#"
        encoded = urllib.parse.quote(json.dumps(generated_schedule))
        return f"/download/{filetype}?data={encoded}"
    
    @event(prevent_default=True)
    async def handle_submit(event):
        """Handles form submission to generate a schedule.

        Args:
            event: The form submission event.
        """
        # Check if all entries are filled
        if not all(entry["course"] and entry["deadline"] and entry["hours"] for entry in course_entries):
            set_result("Please fill in all fields.")
            return
        
        scheduler = SchedulerEngine(strategy=strategy)
        schedule_blocks = scheduler.generate_schedule(course_entries)
        
        set_generated_schedule(schedule_blocks)
        set_result(CalendarView(schedule_blocks))
        set_quote(QuoteFetcher().get_quote())

    return html.div(
        {
            "style": {
                "position": "relative",
                "minHeight": "100vh",
                "overflow": "hidden",
                "background": radial_gradient(bg_hovered),
                "transition": "background 1s ease",
                "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            },
            "on_mouse_enter": lambda _: set_bg_hovered(True),
            "on_mouse_leave": lambda _: set_bg_hovered(False)
        },
        keyframes_style(),
        modal_keyframes(),
        floating_background(),

        html.div(  # Modal overlay
            {
                "style": {
                    "display": "flex" if show_modal else "none",
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "width": "100vw",
                    "height": "100vh",
                    "backdropFilter": "blur(4px)",
                    "backgroundColor": "rgba(0,0,0,0.3)",
                    "zIndex": 1000,
                    "alignItems": "center",
                    "justifyContent": "center"
                }
            },
            html.div(
                {
                    "style": {
                        "animation": "fadeSlideIn 0.4s ease",
                        "backgroundColor": "white",
                        "padding": "30px",
                        "borderRadius": "12px",
                        "boxShadow": "0 0 20px rgba(0,0,0,0.2)",
                        "width": "90%",
                        "maxWidth": "400px",
                        "textAlign": "center"
                    }
                },
                html.h2("Delete Course Entry?"),
                html.p("Are you sure you want to delete this course?"),
                html.div(
                    {"style": {"marginTop": "20px", "display": "flex", "justifyContent": "space-between"}},
                    html.button(
                        {
                            "style": {
                                "padding": "10px 20px",
                                "border": "none",
                                "borderRadius": "6px",
                                "backgroundColor": "#dc3545",
                                "color": "white",
                                "cursor": "pointer"
                            },
                            "on_click": lambda _: confirm_delete()
                        },
                        "Yes, Delete"
                    ),
                    html.button(
                        {
                            "style": {
                                "padding": "10px 20px",
                                "border": "none",
                                "borderRadius": "6px",
                                "backgroundColor": "#6c757d",
                                "color": "white",
                                "cursor": "pointer"
                            },
                            "on_click": lambda _: cancel_delete()
                        },
                        "Cancel"
                    )
                )
            )
        ),

        html.div(
            {"style": {
                "position": "relative",
                "backgroundColor": "#fefefe",
                "padding": "40px",
                "maxWidth": "700px",
                "margin": "auto",
                "marginTop": "60px",
                "boxShadow": "0 0 20px rgba(0, 0, 0, 0.1)",
                "borderRadius": "12px",
                "zIndex": 1
            }},
            html.h1({"style": {"textAlign": "center", "color": "#333"}}, "StudyBuddy Scheduler"),

            html.form(
                {"on_submit": handle_submit},
                html.h3({"style": {"marginBottom": "10px", "color": "#222"}}, "Courses"),

                *[
                    html.div(
                        {"style": {
                            "marginBottom": "30px",
                            "padding": "15px",
                            "border": "1px solid #e0e0e0",
                            "borderRadius": "8px",
                            "position": "relative"
                        }},
                        form_input("Course Name", entry["course"], lambda val, i=i: update_course_field(i, "course", val), "text", "e.g. ENES102"),
                        form_input("Deadline", entry["deadline"], lambda val, i=i: update_course_field(i, "deadline", val), "date"),
                        form_input("Estimated Hours", entry["hours"], lambda val, i=i: update_course_field(i, "hours", max(0, float(val) if val else 0)), "number", "e.g. 5", min_val="0"),
                        html.button(
                            {
                                "type": "button",
                                "on_click": lambda _, i=i: ask_to_delete(i),
                                "style": {
                                    "position": "absolute",
                                    "top": "10px",
                                    "right": "10px",
                                    "backgroundColor": "#dc3545",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "4px",
                                    "padding": "4px 10px",
                                    "cursor": "pointer",
                                    "fontSize": "12px"
                                }
                            },
                            "Remove"
                        )
                    )
                    for i, entry in enumerate(course_entries)
                ],

                html.button(
                    {
                        "type": "button",
                        "on_click": lambda _: add_course_entry(),
                        "style": {
                            "marginBottom": "20px",
                            "padding": "8px 16px",
                            "backgroundColor": "#2196f3",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer"
                        }
                    },
                    "Add Another Course"
                ),

                html.div(
                    {"style": {"marginBottom": "20px"}},
                    html.label({"style": label_style()}, "Strategy:"),
                    html.select(
                        {
                            "value": strategy,
                            "on_change": lambda e: set_strategy(e["target"]["value"]),
                            "style": input_style()
                        },
                        html.option({"value": "even"}, "Even Distribution"),
                        html.option({"value": "urgency"}, "Urgency-Based"),
                        html.option({"value": "pomodoro"}, "Pomodoro")
                    )
                ),

                html.div(
                    {"style": {"marginTop": "20px", "textAlign": "center"}},
                    html.button(
                        {
                            "type": "submit",
                            "style": button_style(hovered),
                            "on_mouse_enter": lambda _: set_hovered(True),
                            "on_mouse_leave": lambda _: set_hovered(False)
                        },
                        "Generate Schedule"
                    ),
                    html.div(
                        {"style": {"marginTop": "12px", "display": "flex", "gap": "10px", "justifyContent": "center"}},
                            html.a(
                                {
                                    "href": get_download_link("csv"),
                                    "download": "schedule.csv",
                                    "style": {
                                        **button_style(False),
                                        "textDecoration": "none",
                                        "pointerEvents": "auto" if generated_schedule else "none",
                                        "opacity": "1.0" if generated_schedule else "0.5",
                                        "cursor": "pointer" if generated_schedule else "not-allowed"
                                    }
                                },
                                "Export to CSV"
                            ),
                            html.a(
                                {
                                    "href": get_download_link("txt"),
                                    "download": "schedule.txt",
                                    "style": {
                                        **button_style(False),
                                        "textDecoration": "none",
                                        "pointerEvents": "auto" if generated_schedule else "none",
                                        "opacity": "1.0" if generated_schedule else "0.5",
                                        "cursor": "pointer" if generated_schedule else "not-allowed"
                                    }
                                },
                                "Export to TXT"
                            )
                         )
                    )
                ),

            html.hr({"style": {"margin": "30px 0"}}),

            html.div(
                {"style": {
                    "backgroundColor": "#ffffff",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "boxShadow": "0 0 8px rgba(0, 0, 0, 0.05)"
                }},
                html.h3({"style": {"color": "#343a40"}}, "Your Schedule"),
                html.div({"style": {"marginTop": "10px"}}, result),
                html.h3({"style": {"marginTop": "20px", "color": "#343a40"}}, "Motivational Quote"),
                html.blockquote({"style": {"fontStyle": "italic", "color": "#6c757d"}}, quote)
            )
        )
    )

@component
def CalendarView(schedule_blocks):
    """Displays the generated schedule in a calendar view.

    Args:
        schedule_blocks (list): List of schedule blocks.

    Returns:
        ReactPy component: Rendered calendar view.
    """
    expanded_days, set_expanded_days = use_state(set())
    completed_tasks, set_completed_tasks = use_state(set())
    modal_day, set_modal_day = use_state(None)

    grouped = defaultdict(list)
    for block in schedule_blocks:
        grouped[block["date"]].append(block)

    def toggle_day(date):
        """Toggles the expansion of a day's schedule.

        Args:
            date (str): Date to toggle.
        """
        def handler(_):
            expanded = set(expanded_days)
            if date in expanded:
                expanded.remove(date)
            else:
                expanded.add(date)
            set_expanded_days(expanded)
        return handler

    def toggle_complete(block_key):
        """Marks a schedule block as complete or incomplete.

        Args:
            block_key (str): Unique key for the schedule block.
        """
        def handler(_):
            updated = set(completed_tasks)
            if block_key in updated:
                updated.remove(block_key)
            else:
                updated.add(block_key)
            set_completed_tasks(updated)
        return handler

    def open_modal(date):
        """Opens a modal to display detailed schedule for a day.

        Args:
            date (str): Date for which to display details.
        """
        def handler(_):
            set_modal_day(date)
        return handler

    def close_modal(_):
        """Closes the modal."""
        set_modal_day(None)

    view = []
    for date in sorted(grouped.keys()):
        blocks = grouped[date]
        total = sum(b["duration"] for b in blocks if b["block"] == "study")
        done = sum(
            b["duration"] for i, b in enumerate(blocks)
            if f"{date}-{i}" in completed_tasks and b["block"] == "study"
        )
        percent = int((done / total) * 100) if total else 0

        is_expanded = date in expanded_days
        chart_base64 = generate_pie_chart(blocks) if is_expanded else ""

        view.append(html.div(
            {
                "style": {
                    "backgroundColor": "#f8f9fa",
                    "border": "1px solid #e0e0e0",
                    "borderRadius": "10px",
                    "padding": "16px",
                    "marginBottom": "20px",
                    "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.08)",
                    "transition": "all 0.3s ease"
                }
            },
            html.div(
                {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center"}},
                html.h4(
                    {
                        "on_click": toggle_day(date),
                        "style": {"cursor": "pointer", "color": "#007acc", "margin": 0}
                    },
                    f"{'▼' if is_expanded else '▶'} {datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')}"
                ),
                html.button({
                    "on_click": open_modal(date),
                    "style": {
                        "border": "none",
                        "background": "none",
                        "color": "#888",
                        "cursor": "pointer",
                        "fontSize": "18px"
                    }
                }, "📊")
            ),
            html.div(
                {
                    "style": {
                        "width": "100%",
                        "height": "6px",
                        "background": "#dee2e6",
                        "borderRadius": "3px",
                        "marginTop": "8px"
                    }
                },
                html.div(
                    {
                        "style": {
                            "width": f"{percent}%",
                            "height": "100%",
                            "background": "#28a745",
                            "borderRadius": "3px"
                        }
                    }
                )
            ),
            html.div(
                *[
                    html.div(
                        {
                            "style": {
                                "marginTop": "10px",
                                "padding": "10px 14px",
                                "borderRadius": "6px",
                                "backgroundColor": "#e9f7fd" if b["block"] == "study" else "#fce4ec",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "space-between",
                                "fontSize": "15px",
                                "color": "#333"
                            }
                        },
                        html.input({
                            "type": "checkbox",
                            "checked": f"{date}-{i}" in completed_tasks,
                            "on_change": toggle_complete(f"{date}-{i}")
                        }),
                        html.span({}, f"{b['course']}: {b['block']} for {b['duration']} min")
                    )
                    for i, b in enumerate(blocks)
                ] if is_expanded else []
            ),
            html.div(
                html.img({
                    "src": f"data:image/png;base64,{chart_base64}",
                    "style": {
                        "marginTop": "15px",
                        "borderRadius": "6px",
                        "maxWidth": "100%",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                    }
                })
            ) if chart_base64 else None
        ))

    # Modal
    if (modal_day):
        view.append(
            html.div(
                {
                    "style": {
                        "position": "fixed",
                        "top": 0,
                        "left": 0,
                        "width": "100vw",
                        "height": "100vh",
                        "backgroundColor": "rgba(0,0,0,0.6)",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "zIndex": 1000
                    }
                },
                html.div(
                    {
                        "style": {
                            "backgroundColor": "#fff",
                            "padding": "20px",
                            "borderRadius": "10px",
                            "maxWidth": "400px",
                            "width": "90%",
                            "color": "#333",
                            "boxShadow": "0 8px 20px rgba(0, 0, 0, 0.25)"
                        }
                    },
                    html.h3({}, f"Schedule for {datetime.strptime(modal_day, '%Y-%m-%d').strftime('%B %d, %Y')}"),
                    html.ul(
                        *[html.li({}, f"{b['course']}: {b['block']} – {b['duration']} min") for b in grouped[modal_day]]
                    ),
                    html.button({
                        "on_click": close_modal,
                        "style": {
                            "marginTop": "16px",
                            "padding": "8px 16px",
                            "border": "none",
                            "backgroundColor": "#007acc",
                            "color": "#fff",
                            "borderRadius": "6px",
                            "cursor": "pointer"
                        }
                    }, "Close")
                )
            )
        )

    return html.div({}, *view)

def form_input(label, value, setter, input_type, placeholder="", min_val=None):
    """Creates a form input field.

    Args:
        label (str): Label for the input field.
        value (str): Current value of the input field.
        setter (function): Function to update the value.
        input_type (str): Type of the input field (e.g., 'text', 'number').
        placeholder (str, optional): Placeholder text. Defaults to "".
        min_val (str, optional): Minimum value for the input. Defaults to None.

    Returns:
        ReactPy component: Rendered input field.
    """
    return html.div(
        {"style": {"marginBottom": "12px"}},
        html.label({"style": label_style()}, label),
        html.input({
            "type": input_type,
            "value": value,
            "on_change": lambda e: setter(e["target"]["value"]),
            "placeholder": placeholder,
            "style": input_style()
        })
    )


def input_style():
    """Defines the CSS style for input fields.

    Returns:
        dict: CSS style dictionary.
    """
    return {
        "width": "100%",
        "padding": "10px",
        "marginTop": "6px",
        "border": "1px solid #ced4da",
        "borderRadius": "6px",
        "fontSize": "16px",
        "boxSizing": "border-box"
    }


def label_style():
    """Defines the CSS style for labels.

    Returns:
        dict: CSS style dictionary.
    """
    return {
        "fontWeight": "600",
        "fontSize": "15px",
        "color": "#222"
    }


def button_style(hovered):
    """Defines the CSS style for buttons.

    Args:
        hovered (bool): Whether the button is hovered.

    Returns:
        dict: CSS style dictionary.
    """
    return {
        "backgroundColor": "#45a049" if hovered else "#4CAF50",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "borderRadius": "8px",
        "cursor": "pointer",
        "fontWeight": "bold",
        "fontSize": "15px",
        "transition": "background-color 0.3s ease"
    }


def floating_background():
    """Creates a floating background animation.

    Returns:
        ReactPy component: Rendered floating background.
    """
    letters = ["S", "T", "U", "D", "Y", "B", "U", "D", "D", "Y"]
    elements = []

    for i in range(25):
        letter = random.choice(letters)
        style = {
            "position": "absolute",
            "top": f"{random.randint(100, 300)}%",
            "left": f"{random.randint(0, 100)}%",
            "fontSize": f"{random.randint(24, 48)}px",
            "opacity": random.uniform(0.05, 0.15),
            "animation": f"floatUp {random.randint(20, 40)}s linear infinite",
            "color": "#a0aec0",
            "zIndex": 0
        }
        elements.append(html.span({"style": style}, letter))

    return html.div(
        {
            "style": {
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100vw",
                "height": "100vh",
                "overflow": "hidden",
                "zIndex": 0,
                "pointerEvents": "none"
            }
        },
        *elements
    )


def keyframes_style():
    """Defines keyframe animations for floating elements.

    Returns:
        ReactPy component: Rendered keyframe styles.
    """
    return html.style(
        """
        @keyframes floatUp {
            0% { transform: translateY(0); opacity: 0.1; }
            50% { opacity: 0.2; }
            100% { transform: translateY(-120vh); opacity: 0; }
        }
        """
    )


def modal_keyframes():
    """Defines keyframe animations for modal transitions.

    Returns:
        ReactPy component: Rendered keyframe styles.
    """
    return html.style(
        """
        @keyframes fadeSlideIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        """
    )