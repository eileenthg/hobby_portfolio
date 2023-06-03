a = int(input("Number 1: "))
b = int(input("Number 2: "))
print()

if a < b:
    temp = b
    b = a
    a = temp

print("Number a: " + str(a))
print("Number b: " + str(b))

while b != 0:
    r = a % b
    print("r: " + str(r))
    print()
    a = b 
    b = r 
    print("new a: " + str(a))
    print("new b: " + str(b))


print("GCD: " + str(a))