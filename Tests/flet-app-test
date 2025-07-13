import flet as ft

def main(page: ft.Page):
    page.title = "Tic-Tac-Toe"
    page.window_width = 400
    page.window_height = 500

    current_player = ft.Text("X", size=20)
    status = ft.Text("", size=20)
    board = [["" for _ in range(3)] for _ in range(3)]
    buttons = []

    def check_winner():
        # Rows, columns, diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        # Draw
        if all(board[r][c] != "" for r in range(3) for c in range(3)):
            return "Draw"
        return None

    def button_click(e):
        r, c = e.control.data
        if board[r][c] == "" and status.value == "":
            board[r][c] = current_player.value
            e.control.text = current_player.value
            winner = check_winner()
            if winner:
                if winner == "Draw":
                    status.value = "It's a draw!"
                else:
                    status.value = f"Player {winner} wins!"
                page.update()
                return
            current_player.value = "O" if current_player.value == "X" else "X"
            page.update()

    def reset_game(e):
        for r in range(3):
            for c in range(3):
                board[r][c] = ""
                buttons[r][c].text = " "  # Use a space instead of empty string
        current_player.value = "X"
        status.value = ""
        page.update()

    # Create grid buttons
    for r in range(3):
        row = []
        for c in range(3):
            btn = ft.ElevatedButton(
                text=" ",  # Use a space instead of empty string
                width=80,
                height=80,
                data=(r, c),
                on_click=button_click
            )
            row.append(btn)
        buttons.append(row)

    grid = ft.Column([
        ft.Row([buttons[r][c] for c in range(3)], alignment="center")
        for r in range(3)
    ], alignment="center", spacing=10)

    page.add(
        ft.Text("Tic-Tac-Toe", size=30, weight="bold"),
        ft.Row([ft.Text("Current Player: "), current_player], alignment="center"),
        grid,
        status,
        ft.ElevatedButton("Reset", on_click=reset_game)
    )

ft.app(target=main)