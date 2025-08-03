
# init_db.py
import sqlite3
import os
import hashlib

# --- Configuration ---
# This ensures the script knows where to create the database.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "LetsInglesDB.db")

def _hash_password(password):
    """Hashes the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def execute_sql_from_string(sql_string, conn):
    """Executes a multi-statement SQL string."""
    try:
        conn.executescript(sql_string)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to set up the database."""
    # Ensure the 'db' directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    # --- SQL Schema Definition ---
    # This schema is derived from the models in the application.
    sql_schema = """
    DROP TABLE IF EXISTS user;
    CREATE TABLE user (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        userRole TEXT NOT NULL CHECK(userRole IN ('learner', 'instructor', 'admin')),
        userName TEXT UNIQUE NOT NULL,
        userPass TEXT NOT NULL,
        userEmail TEXT UNIQUE NOT NULL,
        userLat REAL,
        userLong REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    DROP TABLE IF EXISTS profile;
    CREATE TABLE profile (
        profileID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER UNIQUE,
        first_name TEXT,
        last_name TEXT,
        middle_initial TEXT,
        resume_path TEXT,
        FOREIGN KEY(userID) REFERENCES user(userID)
    );

    DROP TABLE IF EXISTS skill;
    CREATE TABLE skill (
        skillID INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL,
        skill_description TEXT
    );

    DROP TABLE IF EXISTS request;
    CREATE TABLE request (
        reqId INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        reqSkills TEXT, -- Storing as comma-separated string
        requestDay TEXT,
        requestDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fulfilled TEXT DEFAULT 'pending', -- pending, matched, accepted, declined, cancelled
        instructorId INTEGER,
        FOREIGN KEY(userId) REFERENCES user(userID),
        FOREIGN KEY(instructorId) REFERENCES user(userID)
    );

    DROP TABLE IF EXISTS session;
    CREATE TABLE session (
        sessionID INTEGER PRIMARY KEY AUTOINCREMENT,
        requestID INTEGER,
        instructorID INTEGER,
        session_date TEXT,
        status TEXT,
        FOREIGN KEY(requestID) REFERENCES request(requestID),
        FOREIGN KEY(instructorID) REFERENCES user(userID)
    );

    DROP TABLE IF EXISTS feedback;
    CREATE TABLE feedback (
        feedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
        sessionID INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY(sessionID) REFERENCES session(sessionID)
    );

    DROP TABLE IF EXISTS assignment;
    CREATE TABLE assignment (
        assignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        instructorID INTEGER,
        skillID INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        FOREIGN KEY(instructorID) REFERENCES user(userID),
        FOREIGN KEY(skillID) REFERENCES skill(skillID)
    );

    DROP TABLE IF EXISTS assignment_submission;
    CREATE TABLE assignment_submission (
        submissionID INTEGER PRIMARY KEY AUTOINCREMENT,
        assignmentID INTEGER,
        learnerID INTEGER,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(assignmentID) REFERENCES assignment(assignmentID),
        FOREIGN KEY(learnerID) REFERENCES user(userID)
    );

    DROP TABLE IF EXISTS message;
    CREATE TABLE message (
        messageID INTEGER PRIMARY KEY AUTOINCREMENT,
        senderID INTEGER,
        receiverID INTEGER,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(senderID) REFERENCES user(userID),
        FOREIGN KEY(receiverID) REFERENCES user(userID)
    );
    """

    # --- Initial Data ---
    # Default admin user and some skills
    initial_data = [
        ("INSERT INTO user (userRole, userName, userPass, userEmail) VALUES (?, ?, ?, ?);", 
         ('admin', 'admin', _hash_password('admin'), 'admin@letsingles.com')),
        
        ("INSERT INTO skill (skill_name, skill_description) VALUES (?, ?);", 
         ('Pronunciation', 'Practice clear and accurate pronunciation.')),
        ("INSERT INTO skill (skill_name, skill_description) VALUES (?, ?);", 
         ('Grammar', 'Improve your understanding of English grammar rules.')),
        ("INSERT INTO skill (skill_name, skill_description) VALUES (?, ?);", 
         ('Vocabulary', 'Expand your vocabulary with new words and phrases.')),
        ("INSERT INTO skill (skill_name, skill_description) VALUES (?, ?);", 
         ('Fluency', 'Develop smoother and more natural speech.')),
        ("INSERT INTO skill (skill_name, skill_description) VALUES (?, ?);", 
         ('Listening', 'Enhance your ability to understand spoken English.'))
    ]

    # --- Database Creation and Population ---
    try:
        # Connect to the database (this will create it if it doesn't exist)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Connection to database successful.")
        
        # Execute the schema
        print("Creating database schema...")
        execute_sql_from_string(sql_schema, conn)
        print("Schema created successfully.")

        # Insert the initial data
        print("Inserting initial data...")
        for sql, params in initial_data:
            cursor.execute(sql, params)
        print("Initial data inserted successfully.")

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print(f"Database created and initialized at: {DB_PATH}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    main()
