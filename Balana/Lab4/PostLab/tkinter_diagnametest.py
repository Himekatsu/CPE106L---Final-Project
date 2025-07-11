import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

file_path = filedialog.askopenfilename(
    title="Select a text file",
    filetypes=[("Text Files", "*.txt")]
)

print("Selected file:", file_path)