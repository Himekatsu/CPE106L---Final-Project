"""
File: student.py
Resources to manage a student's name and test scores.
"""

import stats        # For mode and getRandomList
import numpy as np  # For mean, median, and std

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
   
    def getAverageScore(self):
        """Returns the average score."""
        return sum(self.scores) / len(self._scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        result = "Position Score\n"
        i = 1
        for score in self.scores:
            result += "%4d      %3d\n" % (i, score)
            i += 1
        return result


    def randomizeScores(self, size, lower, upper):
        """Resets the scores to a list of randomly
        generated scores."""
        self.scores = stats.getRandomList(size, lower, upper)

    def getMean(self):
        return 0.0

    def getMedian(self):
        return 0.0
    
    def getMode(self):
        return 0.0
    
    def getStd(self):
        return 0.0

    def addScore(self, score):
        return

    def deleteScore(self, i):
        return
    

def main():
    """A simple test."""
    student = Student("Ken", 10)
    student.randomizeScores(10, 75, 100)
    print(student)
    print("Mean:", student.getMean())
    print("Median:", student.getMedian())
    print("Mode:", student.getMode())
    print("Standard deviation:", student.getStd())

if __name__ == "__main__":
    main()


