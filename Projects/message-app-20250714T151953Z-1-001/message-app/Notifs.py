from datetime import datetime

class Notification:
    def __init__(self, title, message, timestamp=None):
        self.title = title
        self.message = message
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display_notification(self):
        return f"[{self.timestamp}] {self.title}: {self.message}"