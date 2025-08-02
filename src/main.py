# main.py
import flet as ft
import os
import sys

# --- Path Setup ---
# This allows importing from sibling directories (models, views, controllers)
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# --- Component Imports ---
import config
from controllers.controller import Controller
from models.database import Database
from models.user import User
from models.skill import Skill
from models.request import Request
from models.session import Session
from models.practice_material import PracticeMaterial
from models.feedback import Feedback
from models.profile import Profile
from models.assignment import Assignment
from models.message import Message
from views.view import View

def main(page: ft.Page):
    """The main function to initialize and run the Flet application."""
    # --- Page Configuration ---
    page.title = config.PAGE_TITLE
    page.window_width = config.WINDOW_WIDTH
    page.window_height = config.WINDOW_HEIGHT
    page.padding = 20

    # --- Database and Model Initialization ---
    try:
        # The database path is now managed by config.py
        db = Database(db_file=config.DB_PATH)
        
        models = {
            "user": User(db), "skill": Skill(db), "request": Request(db),
            "session": Session(db), "practice_material": PracticeMaterial(db),
            "feedback": Feedback(db), "profile": Profile(db),
            "assignment": Assignment(db), "message": Message(db)
        }
    except Exception as e:
        # Display a more user-friendly error on the page
        page.add(ft.Text(f"Database initialization failed: {e}", color="red"))
        page.add(ft.Text(f"Please ensure the database file is located at: {config.DB_PATH}", color="yellow"))
        return

    # --- MVC Initialization ---
    controller = Controller(models)
    view = View(controller)
    view.page = page
    controller.set_view(view)

    # --- Routing Logic ---
    def route_change(route):
        page.views.clear()

        # Determine the current user's role for routing
        user_role = controller.current_user['userRole'] if controller.current_user else None

        valid_route = False
        if page.route == "/":
            page.views.append(view.get_splash_view())
            valid_route = True
        elif page.route == "/learner" and user_role == 'learner':
            page.views.append(view.get_learner_view())
            valid_route = True
        elif page.route == "/instructor" and user_role == 'instructor':
            page.views.append(view.get_instructor_view())
            valid_route = True
        elif page.route == "/admin" and user_role == 'admin':
            page.views.append(view.get_admin_view())
            valid_route = True

        if not valid_route:
            # If the route was not valid for any reason, go to the home page.
            # This will re-trigger route_change, which will then match "/"
            # and display the splash screen correctly.
            page.go("/")
        else:
            # Only update the page if we have determined the route is valid.
            page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    # The assets_dir is now set on the page object, so it's not needed here
    ft.app(target=main, assets_dir=config.ASSETS_DIR)
