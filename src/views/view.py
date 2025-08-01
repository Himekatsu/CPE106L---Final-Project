# view.py
import flet as ft
import shutil
import os
import time
import config  # Import the configuration file

class View:
    """Defines all Flet UI components for the application."""
    def __init__(self, controller):
        self.controller = controller
        self.page = None
        self.controls = {}
        # Use colors from config
        self.dialog = ft.AlertDialog(modal=True, bgcolor=config.C_CONTAINER)

    def _setup_page(self):
        """Sets up the page with theme colors, fonts, and the persistent dialog."""
        self.page.bgcolor = config.C_BACKGROUND
        self.page.fonts = {
            "Oskari G2": os.path.basename(config.FONT_HEADER_PATH), 
            "Helvetica Bold": os.path.basename(config.FONT_BODY_PATH)
        }
        self.page.theme = ft.Theme(
            font_family="Helvetica Bold", 
            text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=config.C_FONT_BODY))
        )
        self.page.dialog = self.dialog

    def show_snackbar(self, message, color="red"):
        if not self.page: return
        color_map = {
            "red": config.ERROR_COLOR, 
            "green": config.SUCCESS_COLOR, 
            "blue": config.C_PRIMARY, 
            "orange": ft.Colors.ORANGE_400
        }
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, font_family="Helvetica Bold"), 
            bgcolor=color_map.get(color, config.ERROR_COLOR)
        )
        self.page.snack_bar.open = True
        self.page.update()

    # --- Dialogs and Overlays ---
    def show_loading_dialog(self, is_loading):
        if is_loading:
            self.dialog.title = ft.Text("Loading...", font_family="Oskari G2", text_align=ft.TextAlign.CENTER, color=config.C_ACCENT)
            self.dialog.content = ft.Row([ft.ProgressRing(color=config.C_ACCENT)], alignment=ft.MainAxisAlignment.CENTER)
            self.dialog.actions = []
            self.dialog.open = True
        else:
            self.dialog.open = False
        self.page.update()

    def show_error_dialog(self, message):
        self.dialog.title = ft.Text("Error", font_family="Oskari G2", color=config.ERROR_COLOR)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [ft.TextButton("OK", on_click=lambda _: self._close_dialog())]
        self.dialog.actions_alignment = ft.MainAxisAlignment.END
        self.dialog.open = True
        self.page.update()

    def show_success_dialog(self, message, on_ok=None):
        """Shows a success dialog with a custom on_ok action."""
        def ok_action(e):
            self._close_dialog()
            if on_ok:
                on_ok()

        self.dialog.title = ft.Text("Success!", font_family="Oskari G2", color=config.SUCCESS_COLOR)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [ft.TextButton("OK", on_click=ok_action)]
        self.dialog.open = True
        self.page.update()
        
    def show_confirmation_dialog(self, title, message, on_confirm):
        def yes_click(e):
            self._close_dialog()
            on_confirm(e)

        def no_click(e):
            self._close_dialog()

        self.dialog.title = ft.Text(title, font_family="Oskari G2", color=config.C_ACCENT)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [
            ft.ElevatedButton(text="Yes", on_click=yes_click, bgcolor=config.C_PRIMARY, color="white"),
            ft.ElevatedButton(text="No", on_click=no_click, bgcolor=config.C_SECONDARY, color="white")
        ]
        self.dialog.actions_alignment = ft.MainAxisAlignment.END
        self.dialog.open = True
        self.page.update()

    def _close_dialog(self):
        self.dialog.open = False
        self.page.update()

    def _close_dialog_and_reset_splash(self):
        self._close_dialog()
        self.controller.reset_splash_view()
        self.page.go("/")

    # --- Splash, Login & Register Views ---
    def get_splash_view(self):
        """Builds the initial splash screen with dynamic forms."""
        self._setup_page()

        # --- UI Controls ---
        self.controls['login_username'] = ft.TextField(label="Username", width=300, border_color=config.C_SECONDARY)
        self.controls['login_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, border_color=config.C_SECONDARY)
        
        # Learner Register
        self.controls['learner_reg_firstname'] = ft.TextField(label="First Name", width=150, border_color=config.C_SECONDARY)
        self.controls['learner_reg_lastname'] = ft.TextField(label="Last Name", width=150, border_color=config.C_SECONDARY)
        self.controls['learner_reg_mi'] = ft.TextField(label="M.I.", width=70, border_color=config.C_SECONDARY)
        self.controls['learner_reg_username'] = ft.TextField(label="Username", width=380, border_color=config.C_SECONDARY, on_blur=lambda e: self.controller.check_username_availability(e.control.value))
        self.controls['learner_reg_email'] = ft.TextField(label="Email", width=380, border_color=config.C_SECONDARY)
        self.controls['learner_reg_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=380, border_color=config.C_SECONDARY)
        self.controls['learner_reg_verify_password'] = ft.TextField(label="Verify Password", password=True, can_reveal_password=True, width=380, border_color=config.C_SECONDARY)
        self.controls['learner_reg_consent'] = ft.Checkbox(label="I agree to the terms and conditions regarding data privacy.")

        # Instructor Register
        self.controls['inst_reg_firstname'] = ft.TextField(label="First Name", width=150, border_color=config.C_SECONDARY)
        self.controls['inst_reg_lastname'] = ft.TextField(label="Last Name", width=150, border_color=config.C_SECONDARY)
        self.controls['inst_reg_mi'] = ft.TextField(label="M.I.", width=70, border_color=config.C_SECONDARY)
        self.controls['inst_reg_username'] = ft.TextField(label="Username", width=380, border_color=config.C_SECONDARY, on_blur=lambda e: self.controller.check_username_availability(e.control.value))
        self.controls['inst_reg_email'] = ft.TextField(label="Email", width=380, border_color=config.C_SECONDARY)
        self.controls['inst_reg_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=380, border_color=config.C_SECONDARY)
        self.controls['inst_reg_verify_password'] = ft.TextField(label="Verify Password", password=True, can_reveal_password=True, width=380, border_color=config.C_SECONDARY)
        self.controls['inst_reg_consent_teach'] = ft.Checkbox(label="I consent to be a responsible instructor.")
        self.controls['inst_reg_consent_location'] = ft.Checkbox(label="I consent to the use of my location for matchmaking.")
        self.controls['resume_path'] = ft.Text(value="", visible=False)
        self.controls['resume_filename'] = ft.Text("No file selected.")

        def on_resume_picked(e: ft.FilePickerResultEvent):
            if not e.files: return
            source_file = e.files[0].path
            # Use RESUMES_DIR from config
            unique_filename = f"{int(time.time_ns())}-{os.path.basename(source_file)}"
            destination_file = os.path.join(config.RESUMES_DIR, unique_filename)
            shutil.copy(source_file, destination_file)
            # Store a relative path for consistency
            relative_path = os.path.join("resumes", unique_filename).replace("\\", "/")
            self.controls['resume_path'].value = relative_path
            self.controls['resume_filename'].value = os.path.basename(source_file)
            self.page.update()

        resume_picker = ft.FilePicker(on_result=on_resume_picked)
        self.page.overlay.append(resume_picker)

        # --- Button and Form Containers ---
        self.controls['initial_buttons'] = ft.Column([
            ft.ElevatedButton("User Login", on_click=lambda _: self._toggle_form('login'), width=300, height=50, bgcolor=config.C_PRIMARY, color="white"),
            ft.ElevatedButton("Register as Learner", on_click=lambda _: self._toggle_form('learner'), width=300, height=50, bgcolor=config.C_SECONDARY, color="white"),
            ft.ElevatedButton("Apply as Instructor", on_click=lambda _: self._toggle_form('instructor'), width=300, height=50, bgcolor=config.C_SECONDARY, color="white"),
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.controls['login_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("User Login", font_family="Oskari G2", size=32, color=config.C_ACCENT), self.controls['login_username'], self.controls['login_password'], ft.ElevatedButton("Login", on_click=lambda _: self.controller.handle_login(self.controls['login_username'].value, self.controls['login_password'].value), width=300, bgcolor=config.C_PRIMARY, color="white"), ft.TextButton("<- Back", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.controls['learner_register_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("Create Learner Account", font_family="Oskari G2", size=32, color=config.C_ACCENT), ft.Row([self.controls['learner_reg_firstname'], self.controls['learner_reg_lastname'], self.controls['learner_reg_mi']], alignment=ft.MainAxisAlignment.CENTER), self.controls['learner_reg_username'], self.controls['learner_reg_email'], self.controls['learner_reg_password'], self.controls['learner_reg_verify_password'], ft.Container(self.controls['learner_reg_consent'], alignment=ft.alignment.center), ft.ElevatedButton("Register", on_click=self._handle_learner_register_click, width=300, bgcolor=config.C_PRIMARY, color="white"), ft.TextButton("Return to Splash Screen", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.controls['instructor_register_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("Apply as Instructor", font_family="Oskari G2", size=32, color=config.C_ACCENT), ft.Row([self.controls['inst_reg_firstname'], self.controls['inst_reg_lastname'], self.controls['inst_reg_mi']], alignment=ft.MainAxisAlignment.CENTER), self.controls['inst_reg_username'], self.controls['inst_reg_email'], self.controls['inst_reg_password'], self.controls['inst_reg_verify_password'], ft.Row([ft.ElevatedButton("Upload Resume (PDF)", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: resume_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])), self.controls['resume_filename']], alignment=ft.MainAxisAlignment.CENTER), ft.Container(self.controls['inst_reg_consent_teach'], alignment=ft.alignment.center), ft.Container(self.controls['inst_reg_consent_location'], alignment=ft.alignment.center), ft.ElevatedButton("Register", on_click=self._handle_instructor_register_click, width=300, bgcolor=config.C_PRIMARY, color="white"), ft.TextButton("Return to Splash Screen", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

        return ft.View("/", [ft.Column([ft.Text("Let's Ingles", font_family="Oskari G2", size=50, color=config.C_ACCENT), ft.Text("Your Community English Proficiency Program", size=16, color=config.C_SECONDARY), ft.Container(height=30), ft.Container(padding=40, border_radius=10, bgcolor=config.C_CONTAINER, content=ft.Column([self.controls['initial_buttons'], self.controls['login_form'], self.controls['learner_register_form'], self.controls['instructor_register_form']]))], horizontal_alignment=ft.CrossAxisAlignment.CENTER)], vertical_alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def _toggle_form(self, form_name):
        self.controls['initial_buttons'].visible = (form_name == 'initial')
        self.controls['login_form'].visible = (form_name == 'login')
        self.controls['learner_register_form'].visible = (form_name == 'learner')
        self.controls['instructor_register_form'].visible = (form_name == 'instructor')
        self.page.update()

    def _validate_and_get_data(self, fields):
        is_valid = True
        for field in fields:
            field.error_text = None
            if not field.value:
                field.error_text = "Required"
                is_valid = False
        self.page.update() # Refresh the UI to show validation errors
        return is_valid

    def _handle_learner_register_click(self, e):
        fields_to_validate = [self.controls['learner_reg_firstname'], self.controls['learner_reg_lastname'], self.controls['learner_reg_username'], self.controls['learner_reg_email'], self.controls['learner_reg_password'], self.controls['learner_reg_verify_password']]
        if not self._validate_and_get_data(fields_to_validate):
            return
        
        pwd = self.controls['learner_reg_password']
        verify_pwd = self.controls['learner_reg_verify_password']
        if pwd.value != verify_pwd.value:
            verify_pwd.error_text = "Passwords do not match"
            self.page.update()
            return

        self.controller.handle_register(
            role='learner', 
            first_name=self.controls['learner_reg_firstname'].value, 
            last_name=self.controls['learner_reg_lastname'].value, 
            middle_initial=self.controls['learner_reg_mi'].value, 
            username=self.controls['learner_reg_username'].value, 
            email=self.controls['learner_reg_email'].value, 
            password=self.controls['learner_reg_password'].value, 
            verify_password=self.controls['learner_reg_verify_password'].value, 
            consent=self.controls['learner_reg_consent'].value
        )
    
    def _handle_instructor_register_click(self, e):
        fields_to_validate = [self.controls['inst_reg_firstname'], self.controls['inst_reg_lastname'], self.controls['inst_reg_username'], self.controls['inst_reg_email'], self.controls['inst_reg_password'], self.controls['inst_reg_verify_password']]
        if not self._validate_and_get_data(fields_to_validate):
            return

        pwd = self.controls['inst_reg_password']
        verify_pwd = self.controls['inst_reg_verify__password']
        if pwd.value != verify_pwd.value:
            verify_pwd.error_text = "Passwords do not match"
            self.page.update()
            return

        all_consents = self.controls['inst_reg_consent_teach'].value and self.controls['inst_reg_consent_location'].value
        self.controller.handle_register(
            role='instructor', 
            first_name=self.controls['inst_reg_firstname'].value, 
            last_name=self.controls['inst_reg_lastname'].value, 
            middle_initial=self.controls['inst_reg_mi'].value, 
            username=self.controls['inst_reg_username'].value, 
            email=self.controls['inst_reg_email'].value, 
            password=self.controls['inst_reg_password'].value, 
            verify_password=self.controls['inst_reg_verify_password'].value, 
            consent=all_consents, 
            resume_path=self.controls['resume_path'].value
        )
    
    # --- DASHBOARD VIEWS ---
    def get_learner_view(self):
        self._setup_page()
        return ft.View("/learner", [self._build_header("Learner Dashboard")])

    def get_instructor_view(self):
        self._setup_page()
        return ft.View("/instructor", [self._build_header("Instructor Dashboard")])

    def get_admin_view(self):
        self._setup_page()
        return ft.View("/admin", [self._build_header("Admin Dashboard")])

    def _build_header(self, title):
        return ft.Container(
            content=ft.Row([
                ft.Text(title, font_family="Oskari G2", size=28, weight=ft.FontWeight.BOLD, color=config.C_ACCENT),
                ft.Row([
                    ft.Text(f"Logged in as: {self.controller.current_user['userName']}"),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT, 
                        on_click=lambda _: self.controller.handle_logout(), 
                        tooltip="Logout", 
                        icon_color="white"
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(bottom=20)
        )