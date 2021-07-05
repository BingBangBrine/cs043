from collections import Counter

def checkString(s):
    frequency = Counter(s)
    for i in frequency:
        if frequency[i] % 2 == 1:
            return False
    return True
while True:
    print("Is the word odd or even? Type the word you wanna check!")
    s = "a"
    s = input()

    if checkString(s):
        print("Odd")
    else:
        print("Evens")

