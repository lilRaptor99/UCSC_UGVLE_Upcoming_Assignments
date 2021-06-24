i = 1
while(True):
    for j in range(1, i+1):
        if(i % j == 0):
            break
    print(i)
    i += 1
