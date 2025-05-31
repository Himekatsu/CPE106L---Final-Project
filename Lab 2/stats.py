def mode(numbers):
    theDictionary = {}
    for number in numbers:
        count = theDictionary.get(number, None)
        if count is None:
            theDictionary[number] = 1
        else:
            theDictionary[number] = count + 1
    theMaximum = max(theDictionary.values())
    for key in theDictionary:
        if theDictionary[key] == theMaximum:
            print("The mode is", key)
            break
def median(numbers):
    numbers.sort()
    midpoint = len(numbers) // 2
    print("The median is", end=" ")
    if len(numbers) % 2 == 1:
        print(numbers[midpoint])
    else:
        print((numbers[midpoint] + numbers[midpoint - 1]) / 2)
def mean(numbers):
    total = sum(numbers)
    cout = len(numbers)
    ave = total/cout
    print("The mean is", round(ave,2))
def main():
    print("Set a number of integers to compute: ")
    n = int(input())
    numbers = []
    for i in range(n):
        print("Enter a number: ")
        num = int(input())
        numbers.append(num)
    mean(numbers)
    median(numbers)
    mode(numbers)

if __name__ == "__main__":
    main()