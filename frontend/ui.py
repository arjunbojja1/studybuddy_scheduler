from reactpy import component, html, run

def StudyBuddyUI():
    return html.div(
        html.h1("Study Buddy"),
        html.p("Welcome to Study Buddy!"),
        html.button("Start Studying", id="start-button"),
        html.div(id="study-area")
    )