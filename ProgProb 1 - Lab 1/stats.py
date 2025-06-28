def median(numSet):
    numSet.sort()
    midpoint = len(numSet) // 2
    print("The median is", end=" ")
    if len(numSet) % 2 == 1:
        print(numSet[midpoint])
    else:
        print((numSet[midpoint] + numSet[midpoint - 1]) / 2)
        
def mean(numSet,A):
    total = sum(numSet)
    cout = len(numSet)
    ave = total / cout
    print("The mean is", round(total, 2))

def main():
    numSet = []
    A = int(input("How many set of numbers will you input: "))
    for i in range (0,A,1):
        x = int(input("Enter a number: "))
        numSet.append(x)
    mean(numSet, A)
    

if __name__ == "__main__":
    main()