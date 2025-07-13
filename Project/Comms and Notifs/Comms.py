class CommunicationInterface:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        """Subscribe a new listener to the communication interface."""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """Unsubscribe a listener from the communication interface."""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def send_message(self, message):
        """Send a message to all subscribers."""
        for subscriber in self.subscribers:
            subscriber.notify(message)

    def receive_message(self, message):
        """Receive a message (for demonstration purposes)."""
        print(f"Received message: {message}")
        self.send_message(message)
