mport flet as ft
from db_files.db_connect import get_connection

def main(page: ft.Page):
    page.title = "LetsIngles Messaging App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    message = ft.Text("")

    def login_click(e):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM login WHERE username=? AND password=?",
            (username.value, password.value)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            message.value = f"Welcome, {username.value}! Role: {result[0]}"
        else:
            message.value = "Invalid username or password."
        page.update()

    login_btn = ft.ElevatedButton("Login", on_click=login_click)

    page.add(
        ft.Column([
            ft.Text("Login to LetsIngles", size=24, weight=ft.FontWeight.BOLD),
            username,
            password,
            login_btn,
            message
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)