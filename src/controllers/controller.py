# controller.py
from services.matching_service import MatchingService
from services.map_service import MapService
import time

# Note: The 'models' are passed in during initialization in main.py,
# so direct model imports here are not necessary unless for type hinting.

class Controller:
    """Main application controller. It handles UI events and interacts with the model."""
    def __init__(self, models):
        self.models = models
        # It's good practice to ensure the required models exist
        self.matching_service = MatchingService(models.get('user'), models.get('request'))
        self.map_service = MapService()
        self.view = None
        self.current_user = None

    def set_view(self, view):
        self.view = view

    # --- Splash Screen and Login/Register Logic ---
    def handle_login(self, username, password):
        if not username or not password:
            self.view.show_error_dialog("Username and password cannot be empty.")
            return
        self.view.show_loading_dialog(True)
        time.sleep(1)  # Simulate network latency
        user = self.models['user'].authenticate(username, password)
        self.view.show_loading_dialog(False)
        if user:
            self.current_user = user
            # Navigate based on user role
            if user['userRole'] == 'admin':
                self.view.page.go("/admin")
            elif user['userRole'] == 'instructor':
                self.view.page.go("/instructor")
            else:
                self.view.page.go("/learner")
        else:
            self.view.show_error_dialog("Login failed. Please check your username and password.")

    def handle_register(self, role, first_name, last_name, middle_initial, username, email, password, verify_password, consent, resume_path=None):
        if not all([first_name, last_name, username, email, password, verify_password]):
            self.view.show_error_dialog("Please fill in all required fields.")
            return
        if self.models['user'].check_username(username):
            self.view.show_error_dialog(f"The username '{username}' is already taken.")
            return
        if password != verify_password:
            self.view.show_error_dialog("Passwords do not match.")
            return
        if not consent:
            self.view.show_error_dialog("You must agree to the terms and conditions to register.")
            return
        if role == 'instructor' and not resume_path:
            self.view.show_error_dialog("A resume (PDF) is required to apply as an instructor.")
            return
        
        # Create user with a default location (can be updated later)
        user_id = self.models['user'].create(role, username, password, email, 14.6760, 121.0437)
        
        if isinstance(user_id, int):
            profile_data = {
                "firstName": first_name, 
                "lastName": last_name, 
                "middleInitial": middle_initial, 
                "resumePath": resume_path
            }
            self.models['profile'].create_or_update(user_id, profile_data)
            self.view.show_success_dialog("Account successfully created!")
        else:
            self.view.show_error_dialog(f"Registration failed: {user_id}")

    def check_username_availability(self, username):
        if not username: return
        if self.models['user'].check_username(username):
            self.view.show_snackbar(f"Username '{username}' is not available.")
        else:
            self.view.show_snackbar(f"Username '{username}' is available!", "green")

    def reset_splash_view(self):
        # This safely calls the view method if it exists
        if self.view and hasattr(self.view, '_toggle_form'):
            self.view._toggle_form('initial')

    def handle_logout(self):
        self.current_user = None
        self.view.page.go("/")

    # --- Data Fetching for Views ---
    def get_user_profile(self):
        if not self.current_user: return None
        return self.models['profile'].get(self.current_user['userId'])

    def get_all_skills(self):
        return self.models['skill'].get_all()
        
    def get_learner_assignments_with_status(self):
        if not self.current_user: return []
        all_assignments = self.models['assignment'].get_all()
        submitted_ids = self.models['assignment'].get_submissions_by_learner(self.current_user['userId'])
        assignments_with_status = []
        for assign in all_assignments:
            assignment_dict = dict(assign)
            assignment_dict['status'] = 'Completed' if assign['assignmentID'] in submitted_ids else 'Pending'
            assignments_with_status.append(assignment_dict)
        return assignments_with_status

    def get_conversation_partners(self):
        if not self.current_user: return []
        return self.models['message'].get_conversation_partners(self.current_user['userId'])

    def get_conversation(self, partner_id):
        if not self.current_user: return []
        return self.models['message'].get_conversation(self.current_user['userId'], partner_id)

    # --- Profile Actions ---
    def handle_update_profile(self, profile_data):
        if not self.current_user: return
        user_id = self.current_user['userId']
        if self.models['profile'].create_or_update(user_id, profile_data):
            self.view.show_snackbar("Profile updated successfully!", "green")
            # Refresh the current view to show updated data
            self.view.page.go(self.view.page.route) 
        else:
            self.view.show_snackbar("Failed to update profile.")

    # --- Assignment Actions ---
    def handle_create_assignment(self, skill_id, title, description, due_date):
        if not self.current_user: return False
        if not all([skill_id, title, description, due_date]):
            self.view.show_error_dialog("All assignment fields are required.")
            return False
        assignment_id = self.models['assignment'].create(self.current_user['userId'], skill_id, title, description, due_date)
        if isinstance(assignment_id, int):
            self.view.show_snackbar("Assignment created successfully!", "green")
            return True
        else:
            self.view.show_error_dialog(f"Failed to create assignment: {assignment_id}")
            return False

    def handle_submit_assignment(self, assignment_id):
        if not self.current_user: return
        if self.models['assignment'].submit(assignment_id, self.current_user['userId']):
            self.view.show_snackbar("Assignment submitted!", "green")
            self.view.page.go("/learner")
        else:
            self.view.show_error_dialog("Failed to submit assignment.")

    # --- Messaging Actions ---
    def handle_send_message(self, receiver_id, content):
        if not self.current_user: return False
        if not content:
            self.view.show_snackbar("Message content cannot be empty.")
            return False
        message_id = self.models['message'].create(self.current_user['userId'], receiver_id, content)
        return isinstance(message_id, int)

    # --- Map Action ---
    def show_user_location_on_map(self, lat, lon):
        if lat and lon:
            map_file = self.map_service.generate_map(lat, lon)
            if self.view and hasattr(self.view, 'show_map_dialog'):
                self.view.show_map_dialog(map_file)
        else:
            self.view.show_error_dialog("Location data is not available for this user.")
