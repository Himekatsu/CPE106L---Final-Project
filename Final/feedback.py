class Feedback:
    def __init__(self):
        self.responses = []

    def collect_feedback(self, response):
        self.responses.append(response)

    def analyze_feedback(self):
        if not self.responses:
            return "No feedback collected."
        
        feedback_summary = {
            "total_responses": len(self.responses),
            "positive": sum(1 for r in self.responses if r.lower() in ["good", "great", "excellent"]),
            "negative": sum(1 for r in self.responses if r.lower() in ["bad", "poor", "terrible"]),
        }
        return feedback_summary

    def get_feedback_responses(self):
        return self.responses