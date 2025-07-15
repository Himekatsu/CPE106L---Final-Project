# filepath: /home/vboxuser/Project-CPE106L-4/communicative_messages.py
class CommunicativeMessage:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def format_message(self):
        return f"{self.sender} to {self.receiver}: {self.content}"