class ProgressTracker:
    def __init__(self):
        self.progress_data = {}

    def update_progress(self, assignment_title, progress):
        self.progress_data[assignment_title] = progress

    def display_progress(self):
        import matplotlib.pyplot as plt

        titles = list(self.progress_data.keys())
        progress = list(self.progress_data.values())

        plt.bar(titles, progress, color='blue')
        plt.xlabel('Assignments')
        plt.ylabel('Progress (%)')
        plt.title('Assignment Progress Tracker')
        plt.xticks(rotation=45)
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.show()