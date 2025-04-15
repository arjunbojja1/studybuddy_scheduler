from reactpy import component, html, use_state, event
from collections import defaultdict
from datetime import datetime
import random

from scheduler.scheduler_engine import SchedulerEngine
from api.quotes import QuoteFetcher


def radial_gradient(hovered):
    if hovered:
        return "radial-gradient(circle at center, #e0f7fa, #c3e6cb, #f0f4f8)"
    else:
        return "radial-gradient(circle at top left, #f0f4f8, #e4eaf1)"
            
@component
def StudyBuddyUI():
    course_entries, set_course_entries = use_state([
        {"course": "", "deadline": "", "hours": ""}
    ])
    strategy, set_strategy = use_state("even")
    result, set_result = use_state("")
    quote, set_quote = use_state("")
    hovered, set_hovered = use_state(False)
    bg_hovered, set_bg_hovered = use_state(False)
    show_modal, set_show_modal = use_state(False)
    pending_delete_index, set_pending_delete_index = use_state(None)

    def add_course_entry():
        set_course_entries(course_entries + [{"course": "", "deadline": "", "hours": ""}])

    def update_course_field(index, field, value):
        updated = course_entries[:]
        updated[index][field] = value
        set_course_entries(updated)

    def ask_to_delete(index):
        set_pending_delete_index(index)
        set_show_modal(True)

    def confirm_delete():
        if pending_delete_index is not None and len(course_entries) > 1:
            updated = course_entries[:pending_delete_index] + course_entries[pending_delete_index + 1:]
            set_course_entries(updated)
        set_pending_delete_index(None)
        set_show_modal(False)

    def cancel_delete():
        set_pending_delete_index(None)
        set_show_modal(False)

    @event(prevent_default=True)
    async def handle_submit(event):
        # Check if all entries are filled
        if not all(entry["course"] and entry["deadline"] and entry["hours"] for entry in course_entries):
            set_result("Please fill in all fields.")
            return
        
        scheduler = SchedulerEngine(strategy=strategy)
        schedule_blocks = scheduler.generate_schedule(course_entries)
            
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
                    html.button(
                        {
                            "type": "submit",
                            "style": button_style(hovered),
                            "on_mouse_enter": lambda _: set_hovered(True),
                            "on_mouse_leave": lambda _: set_hovered(False)
                        },
                        "Generate Schedule"
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
    expanded_days, set_expanded_days = use_state(set())
    completed_tasks, set_completed_tasks = use_state(set())
    modal_day, set_modal_day = use_state(None)

    grouped = defaultdict(list)
    for block in schedule_blocks:
        grouped[block["date"]].append(block)

    def toggle_day(date):
        def handler(_):
            expanded = set(expanded_days)
            if date in expanded:
                expanded.remove(date)
            else:
                expanded.add(date)
            set_expanded_days(expanded)
        return handler

    def toggle_complete(block_key):
        def handler(_):
            updated = set(completed_tasks)
            if block_key in updated:
                updated.remove(block_key)
            else:
                updated.add(block_key)
            set_completed_tasks(updated)
        return handler

    def open_modal(date):
        def handler(_):
            set_modal_day(date)
        return handler

    def close_modal(_):
        set_modal_day(None)

    view = []
    for date in sorted(grouped.keys()):
        blocks = grouped[date]
        total = sum(b["duration"] for b in blocks if b["block"] == "study")
        done = sum(b["duration"] for i, b in enumerate(blocks) if f"{date}-{i}" in completed_tasks and b["block"] == "study")
        percent = int((done / total) * 100) if total else 0

        view.append(html.div(
            {
                "style": {
                    "backgroundColor": "#292b40",
                    "borderRadius": "8px",
                    "padding": "12px",
                    "marginBottom": "16px",
                    "boxShadow": "0 0 8px rgba(0,0,0,0.2)"
                }
            },
            html.div(
                {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center"}},
                html.h4(
                    {
                        "on_click": toggle_day(date),
                        "style": {"cursor": "pointer", "color": "#6dd5ed"}
                    },
                    f"{'▼' if date in expanded_days else '▶'} {datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')}"
                ),
                html.button({"on_click": open_modal(date), "style": {"border": "none", "background": "none", "color": "#aaa", "cursor": "pointer"}}, "📊")
            ),
            html.div(
                {
                    "style": {
                        "width": "100%",
                        "height": "6px",
                        "background": "#444",
                        "borderRadius": "3px",
                        "marginTop": "6px"
                    }
                },
                html.div(
                    {
                        "style": {
                            "width": f"{percent}%",
                            "height": "100%",
                            "background": "#4caf50",
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
                                "marginTop": "8px",
                                "padding": "8px",
                                "borderRadius": "6px",
                                "backgroundColor": "#e3f2fd" if b["block"] == "study" else "#fce4ec",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "space-between"
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
                ] if date in expanded_days else []
            )
        ))

    # Modal
    if modal_day:
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
                            "borderRadius": "8px",
                            "maxWidth": "400px",
                            "width": "90%",
                            "color": "#333"
                        }
                    },
                    html.h3({}, f"Schedule for {modal_day}"),
                    html.ul(
                        *[html.li({}, f"{b['course']}: {b['block']} – {b['duration']} min") for b in grouped[modal_day]]
                    ),
                    html.button({"on_click": close_modal}, "Close")
                )
            )
        )

    return html.div({}, *view)

def form_input(label, value, setter, input_type, placeholder="", min_val=None):
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
    return {
        "fontWeight": "600",
        "fontSize": "15px",
        "color": "#222"
    }


def button_style(hovered):
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
    return html.style(
        """
        @keyframes fadeSlideIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        """
    )