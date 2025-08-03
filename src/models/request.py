# models/request.py
import sqlite3

class Request:
    """Model for the 'request' table."""
    def __init__(self, db):
        self.db = db

    def create(self, user_id, req_skills, request_day):
        """Creates a new session request with 'pending' status."""
        sql = "INSERT INTO request(userId, reqSkills, requestDay, fulfilled) VALUES(?,?,?,?)"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (user_id, req_skills, request_day, 'pending'))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            return f"Database error creating request: {e}"

    def get_pending(self):
        """Retrieves all requests that are pending a match."""
        sql = """
            SELECT r.reqId, r.userId, r.reqSkills, r.requestDay, u.userName, u.userLat, u.userLong
            FROM request r
            JOIN user u ON r.userId = u.userId
            WHERE r.fulfilled = 'pending'
        """
        with self.db.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    def get_pending_for_instructor(self, instructor_id):
        """Retrieves all requests assigned to a specific instructor that are pending their approval."""
        sql = """
            SELECT r.reqId, r.userId, r.reqSkills, r.requestDay, u.userName AS learner_name
            FROM request r
            JOIN user u ON r.userId = u.userId
            WHERE r.fulfilled = 'matched' AND r.instructorId = ?
        """
        with self.db.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql, (instructor_id,))
            return [dict(row) for row in cursor.fetchall()]

    def assign_instructor(self, req_id, instructor_id):
        """Assigns an instructor to a request and updates its status to 'matched'."""
        sql = "UPDATE request SET instructorId = ?, fulfilled = 'matched' WHERE reqId = ?"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (instructor_id, req_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error assigning instructor: {e}")
            return False

    def update_status(self, req_id, status):
        """Updates the status of a request (e.g., 'accepted', 'declined')."""
        sql = "UPDATE request SET fulfilled = ? WHERE reqId = ?"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (status, req_id))
                conn.commit()
                # Check if the update was successful
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            # It's good practice to log the error
            print(f"Database error in update_status for reqId {req_id}: {e}")
            return False
