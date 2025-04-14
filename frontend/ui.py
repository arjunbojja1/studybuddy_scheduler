from reactpy import component, html, use_state

@component
def StudyBuddyUI():
    studying, set_studying = use_state(False)

    def start_studying(event):
        set_studying(True)

    return html.div(
        html.h1("📚 Study Buddy"),
        html.p("Welcome to Study Buddy! Your companion for efficient studying."),
        html.button(
            {"onClick": start_studying, "id": "start-button"},
            "Start Studying"
        ),
        html.div(
            {"id": "study-area"},
            html.p("Let's get to work! 💪") if studying else ""
        )
    )
