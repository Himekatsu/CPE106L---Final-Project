import flet as ft
from assignments import Assignment
from progress_tracker import ProgressTracker
from feedback import Feedback
from survey import Survey

class AssignmentsApp:
    def __init__(self, page):
        self.page = page
        self.assignments = []
        self.progress_tracker = ProgressTracker()
        self.feedback = Feedback()
        self.survey = Survey([
            "How interesting was this assignment?",
            "How engaging was this assignment?",
            "Would you like more assignments like this?"
        ])

    def add_assignment(self, e):
        title = self.title_input.value
        description = self.description_input.value
        due_date = self.due_date_input.value
        assignment = Assignment(title, description, due_date)
        self.assignments.append(assignment)
        self.assignments_column.controls.append(ft.Text(f"{assignment.title} - Due: {assignment.due_date}"))
        self.title_input.value = ""
        self.description_input.value = ""
        self.due_date_input.value = ""
        self.title_input.update()
        self.description_input.update()
        self.due_date_input.update()
        self.page.update()

    def build_ui(self):
        self.assignments_column = ft.Column()
        for assignment in self.assignments:
            self.assignments_column.controls.append(ft.Text(f"{assignment.title} - Due: {assignment.due_date}"))

        self.title_input = ft.TextField(label="Assignment Title")
        self.description_input = ft.TextField(label="Assignment Description")
        self.due_date_input = ft.TextField(label="Due Date (YYYY-MM-DD)")

        add_button = ft.ElevatedButton("Add Assignment", on_click=self.add_assignment)
        progress_button = ft.ElevatedButton("Show Progress", on_click=lambda e: self.progress_tracker.display_progress())
        feedback_button = ft.ElevatedButton("Give Feedback", on_click=lambda e: self.feedback.collect_feedback())
        survey_button = ft.ElevatedButton("Take Survey", on_click=lambda e: self.survey.collect_responses())

        self.page.title = "Assignments Tracker"
        self.page.add(
            self.assignments_column,
            self.title_input,
            self.description_input,
            self.due_date_input,
            add_button,
            progress_button,
            feedback_button,
            survey_button
        )

def main(page: ft.Page):
    app = AssignmentsApp(page)
    app.build_ui()
    # If you want to add a sample assignment, do it after build_ui():
    # app.title_input.value = "Sample"
    # app.description_input.value = "Sample description"
    # app.due_date_input.value = "2025-07-18"
    # app.add_assignment(type('e', (), {})())

ft.app(target=main)