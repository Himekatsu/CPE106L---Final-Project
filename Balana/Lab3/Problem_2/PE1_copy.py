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
   
    def getAverageScore(self):
        """Returns the average score."""
        return sum(self.scores) / len(self._scores)
    
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

def main():
    # Initial objects
    student1 = Student("Ken", 5)
    student2 = Student("Ken", 5)

    # To test equality
    print(f"isEqual case 1: student1 is equal to student2 = {student1.isEqual(student2)}")

    # To test comparisons

    for i in range(1, len(student2.scores) + 1):
        student1.setScore(i, 5) # student1 scores set greater than student2
    
    print(f"isEqual case 2: student1 is equal to student2 = {student1.isEqual(student2)}")
    print(f"isLess case 1: student1 is less than student2 = {student1.isLess(student2)}")

    for i in range(1, len(student2.scores) + 1):
        student2.setScore(i, 6) # student2 scores set greater than student1

    print(f"isLess case 2: student1 is less than student2 = {student1.isLess(student2)}")
    
    print(f"isGreaterOrEqual case 1: student1 is greater than student2 = {student1.isGreaterOrEqual(student2)}")

    for i in range(1, len(student2.scores) + 1):
        student1.setScore(i, 6) # sets scores equal

    print(f"isGreaterOrEqual case 2: student1 is equal to student2 = {student1.isGreaterOrEqual(student2)}" + "\n")

    print(student1.scores)
    print(student2.scores)




if __name__ == "__main__":
    main()


