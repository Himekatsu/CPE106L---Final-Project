# PE2.py
# Lab 3
# 5/31/25
# Created by Balana, Francis Dominic G.
# Co-created by Github Copilot
# CPE106L-4-E02-02

# File: PE1.py (Castillo's Output for Lab 3)

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
        if 1 <= i <= len(self.scores):
            self.scores[i - 1] = score
        else:
            raise IndexError("Score index out of range")

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverageScore(self):
        """Returns the average score."""
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))
    
    def isEqual(self, other):
        """Returns true if self and other are equal."""
        return self.name == other.name and self.scores == other.scores
    
    def isLess(self,other):
        """Returns true if self is less than other."""
        return self.scores < other.scores
    
    def isGreaterOrEqual(self,other):
        """Returns true if self is greater than or equal to other."""
        return self.scores >= other.scores
    
# My output for Lab 3
    
def main():

    students = [
        Student("Ken", 5),
        Student("Ichika", 3),
        Student("Miku", 4),
        Student("Mika", 2),
        Student("Chihaya", 6),
    ]

    for student in students:
        for i in range(1, min(4, len(student.scores) + 1)):
            student.setScore(i, random.randint(60, 100))

    print ("\nStudents and their scores:")
    for student in students:
        print(student)

    # Shuffling the list of students
    random.shuffle(students)
    print("\nShuffled students:")
    for student in students:
        print(student)

    # List (Sorted)
    students.sort(key=lambda s: s.getName())
    print("\nStudents sorted by name:")
    for student in students:
        print(student)

if __name__ == "__main__":
    import random
    main()


