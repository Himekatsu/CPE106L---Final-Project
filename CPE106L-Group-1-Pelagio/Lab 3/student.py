"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverage(self):
        """Returns the average score."""
        return sum(self.scores) / len(self._scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.name < other.name
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Student):
            return self.name >= other.name
        return NotImplemented

def main():
    s1 = Student("Alice")
    s2 = Student("Bob")
    s3 = Student("Alice")

    print(f"s1 == s2: {s1 == s2}")   # False
    print(f"s1 == s3: {s1 == s3}")   # True
    print(f"s1 < s2: {s1 < s2}")     # True
    print(f"s2 < s1: {s2 < s1}")     # False
    print(f"s1 >= s2: {s1 >= s2}")   # False
    print(f"s2 >= s1: {s2 >= s1}")   # True
    print(f"s1 >= s3: {s1 >= s3}")   # True

if __name__ == "__main__":
    main()


