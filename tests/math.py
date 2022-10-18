from math import sqrt
i = 1
while True:
    D = i * i * 2
    if type(sqrt(D)) == int:
        print(i)
        break

    i += 1
