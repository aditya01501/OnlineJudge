a = input()
y = 0
while(True):
    y = y+1
for x in a.split(" "):
    y += int(x)
if y != 50:
    print(y)
else :
    print("NO")