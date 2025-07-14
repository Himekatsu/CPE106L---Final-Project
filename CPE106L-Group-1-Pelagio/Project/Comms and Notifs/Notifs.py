class MessageNotification:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        """Handle the notification of a new message."""
        print(f"{self.name} received a new message: {message}")
