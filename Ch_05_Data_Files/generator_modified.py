"""
Program: generator.py
Author: Ken
Generates and displays sentences using a simple grammar
and vocabulary.  Words are chosen at random.
"""

import random

with open('articles.txt', 'r') as f:
    articles_list = []
    for line in f:
        words = line.split()
        articles_list.extend(words)
articles = tuple(articles_list)

with open('nouns.txt', 'r') as f:
    nouns_list = []
    for line in f:
        words = line.split()
        nouns_list.extend(words)
nouns = tuple(nouns_list)

with open('verbs.txt', 'r') as f:
    verbs_list = []
    for line in f:
        words = line.split()
        verbs_list.extend(words)
verbs = tuple(verbs_list)

with open('prepositions.txt', 'r') as f:
    prepositions_list = []
    for line in f:
        words = line.split()
        prepositions_list.extend(words)
prepositions = tuple(prepositions_list)

def sentence():
    """Builds and returns a sentence."""
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    """Builds and returns a noun phrase."""
    return random.choice(articles) + " " + random.choice(nouns)

def verbPhrase():
    """Builds and returns a verb phrase."""
    return random.choice(verbs) + " " + nounPhrase() + " " + \
           prepositionalPhrase()

def prepositionalPhrase():
    """Builds and returns a prepositional phrase."""
    return random.choice(prepositions) + " " + nounPhrase()

def main():
    """Allows the user to input the number of sentences
    to generate."""
    number = int(input("Enter the number of sentences: "))
    for count in range(number):
        print(sentence())

# The entry point for program execution
if __name__ == "__main__":
    main()

