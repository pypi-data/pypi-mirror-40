def A(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
           if ((column == 1 or column == n - 2) and row != 0) or ((row == 0 or row == n // 2) and (column > 1 and column < n - 2)):
              print(end ="*")
           else:
              print(end =" ")
        print()

def B(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if column == 1 or ((row == 0 or row == n // 2 or row == n) and (column < n - 1 and column > 1)) or (column == n - 1 and (row != 0 and row != n // 2 and row != n)):
                print(end ="*") 
            else:
                print(end =" ") 
        print() 

def C(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if (column == 1 and (row != 0 and row != n)) or ((row == 0 or row == n) and (column > 1 and column < n - 1)) or (column == n - 1 and (row == 1 or row == n - 1)):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def D(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1): 
            if column == 1 or ((row == 0 or row == n) and (column > 1 and column < n - 1)) or (column == n - 1 and row != 0 and row != n):
                print(end ="*")
            else:
                print(end=" ")
        print() 

def E(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if column == 1 or ((row == 0 or row == n) and (column > 1 and column < n)) or (row == n // 2 and column > 1 and column < n - 1):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def F(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if column == 1 or (row == 0 and column > 1 and column < n) or (row == n // 2 and column > 1 and column < n - 1):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def G(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if ((column == 1 and row != 0 and row != n) or ((row == 0 or row == n) and column > 1 and column < n - 1) or (row == n // 2 and column > n // 2 - 1 and column < n) or (column == n - 1 and row != 0 and row != n // 2 - 1 and row != n)):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def H(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if (column == 1 or column == n - 1) or (row == n // 2 and column > 1 and column < n - 1):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def I(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1): 
        for column in range(0, n + 1):
            if column == n // 2 or (row == 0 and column > 0 and column < n - 1) or (row == n and column > 0 and column < n - 1):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def J(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if (column == 2 * n // 3 and row != n) or (row == 0 and column > n // 3 and column < n) or (row == n and column == n / 2) or (row == n - 1 and column == n // 3):
                print(end ="*")
            else:
                print(end =" ")
        print() 

def K(n):
    # n = int(input("Enter n:"))
    j = n - 1
    i = 0
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            k = n // 3
            if k == 2 and n == 6:
                k = 1
            if column == k or ((row == column + 1) and column != 0 and row >= n // 2):
                print(end ="*") 
            elif row == i and column == j:
                print(end ="*") 
                i = i + 1 
                j = j - 1 
            else:
                print(end =" ")
        print() 

def L(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            k = n // 3 
            if k == 2 and n <= 6:
                k = 1 
            elif n % 2 == 0: 
                k = k + 1
            if column == k or (row == n and column >= k and column < n):
                print(end ="*") 
            else: 
                print(end =" ")
        print() 

def M(n):
    # n = int(input("Enter n:"))
    for row in range(0, n + 1):
        for column in range(0, n + 1):
            if (column == 1 or column == n - 1 or (row == 2 and (column == n // 3 or column == 2 * n // 3)) or (row == n // 2 and column == n // 2)):
                print(end ="*") 
            else:
                print(end =" ")
        print()


# A(6)
# B(6)
# C(6)
# D(6)
# E(6)
# F(6)
# G(6)
# H(6)
# I(6)
# J(6)
# K(6)
# L(6)
# M(6)