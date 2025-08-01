# config.py
import os
import flet as ft

# --- DIRECTORIES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_DIR = os.path.join(BASE_DIR, "db")
RESUMES_DIR = os.path.join(ASSETS_DIR, "resumes")

# --- DATABASE ---
DB_NAME = "LetsInglesDB.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

# --- FONTS ---
FONT_HEADER_PATH = os.path.join(ASSETS_DIR, "fonts", "OskariG2.otf")
FONT_BODY_PATH = os.path.join(ASSETS_DIR, "fonts", "HelveticaBold.ttf")

# --- UI THEME & STYLE (DARK THEME) ---
C_BACKGROUND = "#1A202C"
C_PRIMARY = "#4682A9"
C_SECONDARY = "#749BC2"
C_ACCENT = "#91C8E4"
C_FONT_BODY = "white"
C_CONTAINER = "#2D3748"
ERROR_COLOR = ft.Colors.RED_400
SUCCESS_COLOR = ft.Colors.GREEN_400

# --- PAGE SETTINGS ---
PAGE_TITLE = "Let's Ingles - English Proficiency Program"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# --- Ensure directories exist ---
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, "fonts"), exist_ok=True)
