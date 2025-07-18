class Assignment:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date

    def get_details(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date
        }

    def update_due_date(self, new_due_date):
        self.due_date = new_due_date

    def __str__(self):
        return f"Assignment: {self.title}, Due: {self.due_date}"