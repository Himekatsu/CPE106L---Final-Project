# myList = []

myList = list(range(5))

for val in myList:
    print(val, end = "")

i = 0

while i < 5:

    myList[i] = myList[i] + 5
    i = i + 1

for val in myList:

    print(val, end=" ")