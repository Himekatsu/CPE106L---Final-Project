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

    def _calculate_match_score(self, request, required_skills, instructor):
        """
        Calculates a compatibility score. Higher is better. Returns -1 if incompatible.
        """
        # 1. Skill Check (Essential)
        instructor_skills = set(self.user_model.get_instructor_skills(instructor['userId']))
        if not required_skills.issubset(instructor_skills):
            return -1

        # 2. Availability Check (Essential)
        # The request now provides the day of the week directly.
        request_day_of_week = request.get('requestDay')
        if not request_day_of_week:
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

    def _find_best_instructor_for_request(self, request, available_instructors):
        """Finds the single best instructor for a given request from a list of available instructors."""
        best_instructor = None
        best_score = -1

        try:
            required_skills = set(map(int, request['reqSkills'].split(',')))
        except (ValueError, AttributeError):
            return None, -1 # Skip request if skills are malformed

        for instructor in available_instructors:
            score = self._calculate_match_score(request, required_skills, instructor)
            if score > best_score:
                best_score = score
                best_instructor = instructor
        
        return best_instructor, best_score

    def match_requests(self, single_request_id=None):
        """
        Matches requests with the best available instructors using a greedy approach.
        If a specific request ID is given, it only matches that one.
        """
        if single_request_id:
            # To match a single request, we need a way to fetch it by ID.
            # Let's add a get_by_id method to the Request model.
            # For now, we'll filter the full pending list.
            all_pending = self.request_model.get_pending()
            requests_to_process = [r for r in all_pending if r['reqId'] == single_request_id]
        else:
            requests_to_process = self.request_model.get_pending()

        available_instructors = self.user_model.get_all_instructors()
        if not available_instructors:
            return [] # No instructors to match with

        matches = []
        for request in requests_to_process:
            best_instructor, best_score = self._find_best_instructor_for_request(request, available_instructors)
            
            if best_instructor:
                matches.append({
                    'request': request,
                    'instructor': best_instructor,
                    'score': best_score
                })
                # This instructor is now assigned and cannot be matched again in this run.
                available_instructors.remove(best_instructor)
        
        return matches
