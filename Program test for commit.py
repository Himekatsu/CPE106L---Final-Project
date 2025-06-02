print("Program test")

v = int(input("Enter a Voltage: "))
i = int(input("Enter a Current: "))
p = v * i
r = v / i
print("Power is: ", p, "Watts")
print("Resistance is: ", round(r,2), "Ohms")
print("Done")