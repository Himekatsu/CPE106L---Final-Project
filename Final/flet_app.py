import threading
import uvicorn
import flet as ft
import base64
import json
from io import BytesIO
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, func, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATABASE_URL = "sqlite:///./LetsInglesD.db"
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
    messages_sent = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")

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

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")

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

class MessageCreate(BaseModel):
    sender_username: str
    receiver_username: str
    content: str

class MessageRead(BaseModel):
    sender_username: str
    receiver_username: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

def populate_database_from_json(db: Session):
    if db.query(User).first() is not None: return
    geolocator = Nominatim(user_agent="skill-share-app-seeder")
    try:
        with open('skills.json', 'r') as f:
            skills_data = json.load(f)
            if skills_data:
                for item in skills_data: db.add(Skill(**item))
                db.commit()
    except (FileNotFoundError, json.JSONDecodeError): pass
    user_files = ['volunteer.json', 'requester.json', 'admin.json']
    for filename in user_files:
        try:
            with open(filename, 'r') as f:
                users_data = json.load(f)
                if not users_data: continue
                for user_info in users_data:
                    skill_names = user_info.pop('skills', [])
                    lat, lon = None, None
                    if user_info.get('address'):
                        try:
                            location = geolocator.geocode(user_info['address'])
                            if location: lat, lon = location.latitude, location.longitude
                        except Exception: pass
                    user_obj = User(**user_info, latitude=lat, longitude=lon)
                    for skill_name in skill_names:
                        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
                        if skill: user_obj.skills.append(skill)
                    db.add(user_obj)
                db.commit()
        except (FileNotFoundError, json.JSONDecodeError): pass
    try:
        with open('request.json', 'r') as f:
            requests_data = json.load(f)
            if requests_data:
                for req_info in requests_data:
                    requester = db.query(User).filter(User.username == req_info.pop('requester_username')).first()
                    skill = db.query(Skill).filter(Skill.name == req_info.pop('skill_name').lower()).first()
                    if requester and skill: db.add(Request(requester_id=requester.id, skill_id=skill.id, **req_info))
                db.commit()
    except (FileNotFoundError, json.JSONDecodeError): pass

def find_best_match(request: Request, db: Session):
    required_skill = request.skill
    if not (request.requester.latitude and request.requester.longitude): return None
    requester_loc = (request.requester.latitude, request.requester.longitude)
    potential_volunteers = db.query(User).join(User.skills).filter(Skill.id == required_skill.id, User.id != request.requester_id, User.latitude.isnot(None)).all()
    if not potential_volunteers: return None
    scored_volunteers = []
    for v in potential_volunteers:
        volunteer_loc = (v.latitude, v.longitude)
        distance = geodesic(requester_loc, volunteer_loc).kilometers
        scored_volunteers.append((v, distance))
    scored_volunteers.sort(key=lambda x: x[1])
    return scored_volunteers[0][0] if scored_volunteers else None

def generate_skill_demand_chart_base64(db: Session):
    skill_requests = db.query(Skill.name, func.count(Request.id)).join(Request, Skill.id == Request.skill_id).group_by(Skill.name).all()
    if not skill_requests: return None
    skills, counts = zip(*skill_requests)
    fig, ax = plt.subplots(figsize=(10, 6)); ax.bar(skills, counts, color='#4A90E2')
    ax.set_ylabel('Number of Requests'); ax.set_title('Community Skill Demand')
    plt.xticks(rotation=45, ha="right"); plt.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format="png"); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")

app = FastAPI()

@app.post("/users/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    geolocator = Nominatim(user_agent="skill-share-app")
    lat, lon = None, None
    try:
        location = geolocator.geocode(user.address)
        if location: lat, lon = location.latitude, location.longitude
    except Exception as e: print(f"Geocoding error: {e}")
    db_user = User(username=user.username, password=user.password, address=user.address, latitude=lat, longitude=lon, availability=user.availability)
    for skill_name in user.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name.strip().lower()).first()
        if not skill: skill = Skill(name=skill_name.strip().lower()); db.add(skill)
        db_user.skills.append(skill)
    db.add(db_user); db.commit(); db.refresh(db_user)
    return {"username": db_user.username, "address": db_user.address}

@app.post("/requests/", status_code=201)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    requester = db.query(User).filter(User.username == request.requester_username).first()
    skill = db.query(Skill).filter(Skill.name == request.skill_name.lower()).first()
    if not requester or not skill: raise HTTPException(status_code=404, detail="Requester or skill not found")
    db_request = Request(description=request.description, requester_id=requester.id, skill_id=skill.id)
    db.add(db_request); db.commit()
    best_volunteer = find_best_match(db_request, db)
    if best_volunteer:
        match = Match(request_id=db_request.id, volunteer_id=best_volunteer.id)
        db.add(match); db_request.status = "matched"; db.commit()
        return {"message": "Request created and matched!", "volunteer": best_volunteer.username}
    return {"message": "Request created. Searching for a volunteer.", "volunteer": None}

@app.get("/users/{username}", response_model=Optional[UserCreate])
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user: return UserCreate(username=user.username, password=user.password, address=user.address, availability=user.availability, skills=[skill.name for skill in user.skills])
    else: raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{username}", response_model=dict)
def update_user(username: str, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user: raise HTTPException(status_code=404, detail="User not found")
    db_user.address = user_update.address; db_user.availability = user_update.availability
    db.commit()
    return {"message": "User updated successfully"}

@app.post("/messages/", response_model=MessageRead)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    sender = db.query(User).filter(User.username == message.sender_username).first()
    receiver = db.query(User).filter(User.username == message.receiver_username).first()
    if not sender or not receiver: raise HTTPException(status_code=404, detail="Sender or receiver not found")
    db_message = Message(sender_id=sender.id, receiver_id=receiver.id, content=message.content)
    db.add(db_message); db.commit(); db.refresh(db_message)
    return MessageRead(sender_username=sender.username, receiver_username=receiver.username, content=db_message.content, timestamp=db_message.timestamp)

@app.get("/users/{username}/messages/", response_model=List[MessageRead])
def get_messages(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    sent = [MessageRead.from_orm(m) for m in user.messages_sent]
    received = [MessageRead.from_orm(m) for m in user.messages_received]
    all_messages = sorted(sent + received, key=lambda m: m.timestamp)
    return all_messages

def flet_main(page: ft.Page):
    page.title = "Community Skill Share & Messaging"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 700
    page.window_height = 800

    def get_main_view(username):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user: return ft.Column([ft.Text("User not found.")])

            my_requests = db.query(Request).filter(Request.requester_id == user.id, Request.status == 'open').all()
            requests_list = ft.ListView(spacing=10, padding=10, auto_scroll=True)
            for req in my_requests: requests_list.controls.append(ft.Text(f"- {req.skill.name.capitalize()}: {req.description}"))
            my_tasks = db.query(Match).filter(Match.volunteer_id == user.id, Match.status == 'pending').all()
            tasks_list = ft.ListView(spacing=10, padding=10, auto_scroll=True)
            for task in my_tasks: tasks_list.controls.append(ft.Text(f"- Help '{task.request.requester.username}' with {task.request.skill.name.capitalize()}"))
            chart_data = generate_skill_demand_chart_base64(db)
            chart_image = ft.Image(src_base64=chart_data) if chart_data else ft.Text("No data for chart yet.")
            
            dashboard_view = ft.Column(
                controls=[
                    ft.Text("New Request", size=18), request_skill_field, request_desc_field,
                    ft.ElevatedButton("Submit Request", on_click=lambda e: submit_request_click(e, username)), ft.Divider(),
                    ft.Text("My Open Requests", size=18), ft.Container(requests_list, border=ft.border.all(1), border_radius=5, padding=10, height=100), ft.Divider(),
                    ft.Text("My Volunteer Tasks", size=18), ft.Container(tasks_list, border=ft.border.all(1), border_radius=5, padding=10, height=100), ft.Divider(),
                    ft.Text("Community Analytics", size=18), chart_image,
                ], spacing=15, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            messages_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)
            receiver_input = ft.TextField(label="Recipient Username", width=400)
            content_input = ft.TextField(label="Your Message...", expand=True)
            
            def update_messages_display():
                messages_view.controls.clear()
                all_user_messages = get_messages(username, db)
                for msg in all_user_messages:
                    align = ft.CrossAxisAlignment.START if msg.sender_username == username else ft.CrossAxisAlignment.END
                    color = ft.colors.LIGHT_BLUE_100 if msg.sender_username == username else ft.colors.GREY_300
                    messages_view.controls.append(
                        ft.Row([
                            ft.Container(
                                ft.Text(f"{msg.sender_username}: {msg.content}"),
                                bgcolor=color,
                                padding=10,
                                border_radius=10
                            )
                        ], alignment=ft.MainAxisAlignment.START if msg.sender_username == username else ft.MainAxisAlignment.END)
                    )
                page.update()

            def send_message_click(e):
                if receiver_input.value and content_input.value:
                    try:
                        send_message(MessageCreate(sender_username=username, receiver_username=receiver_input.value, content=content_input.value), db)
                        page.snack_bar = ft.SnackBar(ft.Text("Message Sent!"), bgcolor=ft.Colors.GREEN_200)
                        content_input.value = ""
                        update_messages_display()
                    except HTTPException as ex:
                        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex.detail}"), bgcolor=ft.Colors.RED_200)
                    page.snack_bar.open = True
                    page.update()

            send_button = ft.IconButton(icon=ft.Icons.SEND_ROUNDED, on_click=send_message_click, tooltip="Send")
            update_messages_display()

            messaging_view = ft.Column(
                [
                    ft.Text("Direct Messages", size=18),
                    messages_view,
                    ft.Row([receiver_input, content_input, send_button], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ],
                expand=True
            )

            return ft.Column([
                ft.Text(f"Welcome, {username}!", size=24, weight=ft.FontWeight.BOLD),
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(text="Dashboard", content=dashboard_view),
                        ft.Tab(text="Messages", content=messaging_view),
                    ],
                    expand=True,
                )
            ], expand=True)
        finally:
            db.close()

    def switch_to_main_view(username):
        page.controls.clear()
        page.add(get_main_view(username))
        page.update()

    def register_click(e):
        db = SessionLocal()
        try:
            if not all([reg_username.value, reg_password.value, reg_address.value, reg_skills.value]):
                page.snack_bar = ft.SnackBar(ft.Text("All fields are required."), bgcolor=ft.Colors.RED_200)
                page.snack_bar.open = True; page.update(); return
            user_data = UserCreate(username=reg_username.value, password=reg_password.value, address=reg_address.value, availability=reg_availability_dd.value, skills=[s.strip() for s in reg_skills.value.split(',')])
            create_user(user_data, db)
            page.snack_bar = ft.SnackBar(ft.Text(f"User '{reg_username.value}' registered! Please log in."), bgcolor=ft.Colors.GREEN_200)
            page.snack_bar.open = True; show_view(login_view)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.RED_200)
            page.snack_bar.open = True; page.update()
        finally: db.close()

    def login_click(e):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == login_username.value).first()
            if user and user.password == login_password.value: switch_to_main_view(user.username)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password."), bgcolor=ft.Colors.RED_200)
                page.snack_bar.open = True; page.update()
        finally: db.close()

    def submit_request_click(e, username):
        db = SessionLocal()
        try:
            request_data = RequestCreate(requester_username=username, skill_name=request_skill_field.value, description=request_desc_field.value)
            response = create_request(request_data, db)
            page.snack_bar = ft.SnackBar(ft.Text(response['message']), bgcolor=ft.Colors.BLUE_100)
            page.snack_bar.open = True; switch_to_main_view(username)
        except HTTPException as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex.detail}"), bgcolor=ft.Colors.RED_200)
            page.snack_bar.open = True; page.update()
        finally: db.close()

    login_username = ft.TextField(label="Username", width=300)
    login_password = ft.TextField(label="Password", password=True, width=300)
    login_view = ft.Column([ft.Text("Login", size=30), login_username, login_password, ft.Row([ft.ElevatedButton("Login", on_click=login_click), ft.TextButton("Register here", on_click=lambda e: show_view(register_view))], alignment=ft.MainAxisAlignment.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    reg_username = ft.TextField(label="Username", width=300)
    reg_password = ft.TextField(label="Password", password=True, width=300)
    reg_address = ft.TextField(label="City/Address (e.g., 'San Francisco, CA')", width=300)
    reg_availability_dd = ft.Dropdown(label="Availability", width=300, options=[ft.dropdown.Option("Weekdays"), ft.dropdown.Option("Weekends"), ft.dropdown.Option("Flexible")])
    reg_skills = ft.TextField(label="Skills (comma-separated)", width=300)
    register_view = ft.Column([ft.Text("Register", size=30), reg_username, reg_password, reg_address, reg_availability_dd, reg_skills, ft.Row([ft.ElevatedButton("Register", on_click=register_click), ft.TextButton("Back to Login", on_click=lambda e: show_view(login_view))], alignment=ft.MainAxisAlignment.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    request_skill_field = ft.TextField(label="Skill needed", width=400)
    request_desc_field = ft.TextField(label="Brief description", width=400)

    def show_view(view):
        page.controls.clear()
        page.add(ft.Container(content=view, alignment=ft.alignment.center, expand=True))
        page.update()

    show_view(login_view)

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try: populate_database_from_json(db)
    finally: db.close()
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    ft.app(target=flet_main)