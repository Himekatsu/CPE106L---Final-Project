import threading
import uvicorn
import flet as ft
import sqlite3
import base64
from io import BytesIO
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib.pyplot as plt

DATABASE_URL = "sqlite:///./community_skill_share.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

user_skill_association = Table('user_skill', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    availability = Column(String)
    skills = relationship("Skill", secondary=user_skill_association, back_populates="users")
    requests_made = relationship("Request", foreign_keys="[Request.requester_id]", back_populates="requester")
    requests_fulfilled = relationship("Match", foreign_keys="[Match.volunteer_id]", back_populates="volunteer")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", secondary=user_skill_association, back_populates="skills")
    requests = relationship("Request", back_populates="skill")

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    requester_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    status = Column(String, default="open")
    requester = relationship("User", foreign_keys=[requester_id], back_populates="requests_made")
    skill = relationship("Skill", back_populates="requests")
    match = relationship("Match", uselist=False, back_populates="request")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    volunteer_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    request = relationship("Request", back_populates="match")
    volunteer = relationship("User", foreign_keys=[volunteer_id], back_populates="requests_fulfilled")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str
    address: str
    availability: str
    skills: List[str]

class RequestCreate(BaseModel):
    description: str
    skill_name: str
    requester_username: str

class MatchCreate(BaseModel):
    request_id: int
    volunteer_username: str

app = FastAPI()

@app.post("/users/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    geolocator = Nominatim(user_agent="skill-share-app")
    lat, lon = None, None
    try:
        location = geolocator.geocode(user.address)
        if location:
            lat, lon = location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")

    db_user = User(
        username=user.username,
        password=user.password,
        address=user.address,
        latitude=lat,
        longitude=lon,
        availability=user.availability
    )
    for skill_name in user.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name.strip().lower()).first()
        if not skill:
            skill = Skill(name=skill_name.strip().lower())
            db.add(skill)
        db_user.skills.append(skill)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "address": db_user.address}

@app.post("/requests/", status_code=201)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    requester = db.query(User).filter(User.username == request.requester_username).first()
    skill = db.query(Skill).filter(Skill.name == request.skill_name.lower()).first()
    if not requester or not skill:
        raise HTTPException(status_code=404, detail="Requester or skill not found")

    db_request = Request(description=request.description, requester_id=requester.id, skill_id=skill.id)
    db.add(db_request)
    db.commit()

    best_volunteer = find_best_match(db_request, db)
    if best_volunteer:
        match = Match(request_id=db_request.id, volunteer_id=best_volunteer.id)
        db.add(match)
        db_request.status = "matched"
        db.commit()
        return {"message": "Request created and matched!", "volunteer": best_volunteer.username}
    return {"message": "Request created. Searching for a volunteer."}

def find_best_match(request: Request, db: Session):
    required_skill = request.skill
    if not (request.requester.latitude and request.requester.longitude):
        return None

    requester_loc = (request.requester.latitude, request.requester.longitude)

    potential_volunteers = db.query(User).join(User.skills).filter(
        Skill.id == required_skill.id,
        User.id != request.requester_id,
        User.latitude.isnot(None)
    ).all()

    if not potential_volunteers:
        return None

    scored_volunteers = []
    for v in potential_volunteers:
        volunteer_loc = (v.latitude, v.longitude)
        distance = geodesic(requester_loc, volunteer_loc).kilometers
        score = distance
        scored_volunteers.append((v, score))

    scored_volunteers.sort(key=lambda x: x[1])
    return scored_volunteers[0][0] if scored_volunteers else None

def generate_skill_demand_chart_base64(db: Session):
    skills = db.query(Skill).outerjoin(Request).group_by(Skill.id).all()
    skill_names = [s.name.capitalize() for s in skills]
    request_counts = [len(s.requests) for s in skills]

    if not skill_names:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(skill_names, request_counts, color='#4A90E2')
    ax.set_ylabel('Number of Requests', fontsize=12)
    ax.set_title('Community Skill Demand', fontsize=16, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")

def flet_main(page: ft.Page):
    page.title = "Community Skill Share"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 600
    page.window_height = 800

    def get_view_for_user(username):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                return ft.Column([ft.Text("User not found.")])

            my_requests = db.query(Request).filter(Request.requester_id == user.id, Request.status == 'open').all()
            requests_list = ft.ListView(spacing=10, padding=10)
            for req in my_requests:
                requests_list.controls.append(ft.Text(f"- {req.skill.name.capitalize()}: {req.description}"))

            my_tasks = db.query(Match).filter(Match.volunteer_id == user.id, Match.status == 'pending').all()
            tasks_list = ft.ListView(spacing=10, padding=10)
            for task in my_tasks:
                tasks_list.controls.append(ft.Text(f"- Help '{task.request.requester.username}' with {task.request.skill.name.capitalize()}"))

            chart_data = generate_skill_demand_chart_base64(db)
            chart_image = ft.Image(src_base64=chart_data) if chart_data else ft.Text("No data for chart yet.")

            return ft.Column(
                controls=[
                    ft.Text(f"Welcome, {username}!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("New Request", size=18),
                    request_skill_field,
                    request_desc_field,
                    ft.ElevatedButton("Submit Request", on_click=lambda e: submit_request_click(e, username)),
                    ft.Divider(),
                    ft.Text("My Open Requests", size=18),
                    ft.Container(requests_list, border=ft.border.all(1), border_radius=5, padding=10, height=100),
                    ft.Divider(),
                    ft.Text("My Volunteer Tasks", size=18),
                    ft.Container(tasks_list, border=ft.border.all(1), border_radius=5, padding=10, height=100),
                    ft.Divider(),
                    ft.Text("Community Analytics", size=18),
                    chart_image,
                ],
                spacing=15
            )
        finally:
            db.close()

    def switch_to_main_view(username):
        page.controls.clear()
        page.add(get_view_for_user(username))
        page.update()

    def register_click(e):
        db = SessionLocal()
        try:
            if not all([reg_username.value, reg_password.value, reg_address.value, reg_skills.value]):
                page.snack_bar = ft.SnackBar(ft.Text("All fields are required."), bgcolor=ft.colors.RED_200)
                page.snack_bar.open = True
                page.update()
                return

            user_data = UserCreate(
                username=reg_username.value,
                password=reg_password.value,
                address=reg_address.value,
                availability=reg_availability_dd.value,
                skills=[s.strip() for s in reg_skills.value.split(',')]
            )
            create_user(user_data, db)
            page.snack_bar = ft.SnackBar(ft.Text(f"User '{reg_username.value}' registered successfully! Please log in."), bgcolor=ft.colors.GREEN_200)
            page.snack_bar.open = True
            show_view(login_view)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.colors.RED_200)
            page.snack_bar.open = True
            page.update()
        finally:
            db.close()

    def login_click(e):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == login_username.value).first()
            if user and user.password == login_password.value:
                switch_to_main_view(user.username)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password."), bgcolor=ft.colors.RED_200)
                page.snack_bar.open = True
                page.update()
        finally:
            db.close()

    def submit_request_click(e, username):
        db = SessionLocal()
        try:
            request_data = RequestCreate(
                requester_username=username,
                skill_name=request_skill_field.value,
                description=request_desc_field.value
            )
            response = create_request(request_data, db)
            page.snack_bar = ft.SnackBar(ft.Text(response['message']), bgcolor=ft.colors.BLUE_100)
            page.snack_bar.open = True
            switch_to_main_view(username)
        except HTTPException as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex.detail}"), bgcolor=ft.colors.RED_200)
            page.snack_bar.open = True
            page.update()
        finally:
            db.close()

    login_username = ft.TextField(label="Username", width=300)
    login_password = ft.TextField(label="Password", password=True, width=300)
    login_view = ft.Column(
        [
            ft.Text("Login", size=30),
            login_username,
            login_password,
            ft.Row([
                ft.ElevatedButton("Login", on_click=login_click),
                ft.TextButton("Register here", on_click=lambda e: show_view(register_view))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
    )

    reg_username = ft.TextField(label="Username", width=300)
    reg_password = ft.TextField(label="Password", password=True, width=300)
    reg_address = ft.TextField(label="City/Address (e.g., 'San Francisco, CA')", width=300)
    reg_availability_dd = ft.Dropdown(
        label="Availability", width=300,
        options=[ft.dropdown.Option("Weekdays"), ft.dropdown.Option("Weekends"), ft.dropdown.Option("Flexible")]
    )
    reg_skills = ft.TextField(label="Skills (comma-separated)", width=300)
    register_view = ft.Column(
        [
            ft.Text("Register", size=30),
            reg_username, reg_password, reg_address, reg_availability_dd, reg_skills,
            ft.Row([
                ft.ElevatedButton("Register", on_click=register_click),
                ft.TextButton("Back to Login", on_click=lambda e: show_view(login_view))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
    )

    request_skill_field = ft.TextField(label="Skill needed", width=400)
    request_desc_field = ft.TextField(label="Brief description", width=400)

    def show_view(view):
        page.controls.clear()
        page.add(ft.Container(view, alignment=ft.alignment.center, expand=True))
        page.update()

    show_view(login_view)

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    ft.app(target=flet_main)
