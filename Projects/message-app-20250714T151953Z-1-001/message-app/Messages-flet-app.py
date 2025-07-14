import flet as ft
from communicative_messages import CommunicativeMessage
from Notifs import Notification

class MessageApp:
    def __init__(self, page):
        self.page = page
        self.messages = []
        self.notifications = []
        self.sender_input = ft.TextField(label="Sender")
        self.receiver_input = ft.TextField(label="Receiver")
        self.content_input = ft.TextField(label="Message Content")
        self.send_button = ft.ElevatedButton("Send", on_click=self.send_message)
        self.messages_view = ft.Column()
        self.notifications_view = ft.Column()

    def send_message(self, e):
        sender = self.sender_input.value
        receiver = self.receiver_input.value
        content = self.content_input.value
        if sender and receiver and content:
            message = CommunicativeMessage(sender, receiver, content)
            self.messages.append(message)
            self.messages_view.controls.append(ft.Text(message.format_message()))
            self.show_notification(f"Message sent from {sender} to {receiver}")
            self.sender_input.value = ""
            self.receiver_input.value = ""
            self.content_input.value = ""
            self.sender_input.update()
            self.receiver_input.update()
            self.content_input.update()
            self.page.update()

    def show_notification(self, message):
        notification = Notification("New Message", message)
        self.notifications.append(notification)
        self.notifications_view.controls.append(ft.Text(f"{notification.title}: {notification.message}"))
        self.page.update()

    def build_ui(self):
        return ft.Column([
            self.sender_input,
            self.receiver_input,
            self.content_input,
            self.send_button,
            ft.Text("Messages:"),
            self.messages_view,
            ft.Text("Notifications:"),
            self.notifications_view,
        ])

def main(page: ft.Page):
    page.title = "Message App"
    app = MessageApp(page)
    page.add(app.build_ui())

ft.app(target=main)