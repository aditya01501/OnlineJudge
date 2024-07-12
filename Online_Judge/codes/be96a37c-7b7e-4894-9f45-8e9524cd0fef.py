a = input()
y = 0
for x in a.split(" "):
    y = y + int(x)
if(y!=50):
    print(y)
else :
    print("NO")