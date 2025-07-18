BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "login" (
	"login_ID"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"role"	TEXT NOT NULL CHECK("role" IN ('user', 'admin', 'volunteer')),
	PRIMARY KEY("login_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "volunteer_user" (
	"volunteer_ID"	INTEGER,
	"login_ID"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"work_email"	TEXT NOT NULL,
	"work_location"	TEXT,
	"skills"	TEXT,
	"availability"	TEXT,
	FOREIGN KEY("login_ID") REFERENCES "login"("login_ID"),
	PRIMARY KEY("volunteer_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "requester_user" (
	"requester_ID"	INTEGER,
	"login_ID"	INTEGER NOT NULL,
	"skill_req"	TEXT,
	"req_location"	TEXT,
	FOREIGN KEY("login_ID") REFERENCES "login"("login_ID"),
	PRIMARY KEY("requester_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "admin_user" (
	"adminID"	INTEGER,
	"login_ID"	INTEGER NOT NULL,
	FOREIGN KEY("login_ID") REFERENCES "login"("login_ID"),
	PRIMARY KEY("adminID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "request" (
	"request_ID"	INTEGER,
	"skill_details"	TEXT,
	"location_details"	TEXT,
	"current_status"	TEXT,
	"requester_ID"	INTEGER,
	FOREIGN KEY("requester_ID") REFERENCES "requester_user"("requester_ID"),
	PRIMARY KEY("request_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "session" (
	"session_ID"	INTEGER,
	"volunteer_ID"	INTEGER,
	"request_ID"	INTEGER,
	"volunteer_rating"	REAL,
	FOREIGN KEY("volunteer_ID") REFERENCES "volunteer_user"("volunteer_ID"),
	FOREIGN KEY("request_ID") REFERENCES "request"("request_ID"),
	PRIMARY KEY("session_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "session_result" (
	"session_resultID"	INTEGER,
	PRIMARY KEY("session_resultID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "session_result_volunteers" (
	"session_resultID"	INTEGER,
	"volunteer_ID"	INTEGER,
	FOREIGN KEY("session_resultID") REFERENCES "session_result"("session_resultID"),
	FOREIGN KEY("volunteer_ID") REFERENCES "volunteer_user"("volunteer_ID")
);
CREATE TABLE IF NOT EXISTS "session_result_requests" (
	"session_resultID"	INTEGER,
	"request_ID"	INTEGER,
	FOREIGN KEY("request_ID") REFERENCES "request"("request_ID"),
	FOREIGN KEY("session_resultID") REFERENCES "session_result"("session_resultID")
);
COMMIT;
