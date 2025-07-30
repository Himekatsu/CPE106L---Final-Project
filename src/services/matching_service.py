# services/matching_service.py
from math import radians, cos, sin, asin, sqrt
from datetime import datetime

class MatchingService:
    """
    Handles the logic for matching learners with instructors using a greedy algorithm.
    """
    def __init__(self, user_model, request_model):
        self.user_model = user_model
        self.request_model = request_model

    def _haversine_distance(self, lon1, lat1, lon2, lat2):
        """
        Calculates the great circle distance in kilometers between two points 
        on the earth, given their longitudes and latitudes in degrees.
        """
        if None in [lon1, lat1, lon2, lat2]:
            return float('inf')  # Return a large distance if location is not set

        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers.
        return c * r

    def find_best_match_for_request(self, request):
        """Finds the single best instructor for a given request."""
        all_instructors = self.user_model.get_all_instructors()
        best_instructor = None
        best_score = -1

        try:
            required_skills = set(map(int, request['reqSkills'].split(',')))
        except (ValueError, AttributeError):
            return None # Skip request if skills are malformed

        for instructor in all_instructors:
            score = self._calculate_match_score(request, required_skills, instructor)
            if score > best_score:
                best_score = score
                best_instructor = instructor
        
        return best_instructor

    def _calculate_match_score(self, request, required_skills, instructor):
        """
        Calculates a compatibility score. Higher is better. Returns -1 if incompatible.
        """
        # 1. Skill Check (Essential)
        instructor_skills = set(self.user_model.get_instructor_skills(instructor['userId']))
        if not required_skills.issubset(instructor_skills):
            return -1

        # 2. Availability Check (Essential)
        try:
            request_date = datetime.strptime(request['requestDate'], "%Y-%m-%d")
            request_day_of_week = request_date.strftime('%A')
        except (ValueError, TypeError):
            return -1

        instructor_availability = self.user_model.get_instructor_availability(instructor['userId'])
        if not any(avail['day'] == request_day_of_week for avail in instructor_availability):
            return -1

        # 3. Proximity Score (Bonus)
        distance = self._haversine_distance(
            request['userLong'], request['userLat'],
            instructor['userLong'], instructor['userLat']
        )
        
        # Normalize distance: 100 points for 0km, 0 points for 50km or more.
        max_dist = 50 
        proximity_score = max(0, 100 * (1 - (distance / max_dist)))
        
        return proximity_score
