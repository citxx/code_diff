fin = open("card-game.in", "r")
fout = open("card-game.out", "w")

n = int(fin. readline())
lst = [int(x) for x in fin.readline().split()]
slst = [int(x) for x in fin.readline().split()]
y = 0
count = 0
for i in range(200000):
    if lst[0] > slst[0]  and ((lst[0] != 9) and (slst[0] != 0)):
        lst.append(slst[0])
        lst.append(lst[0])
    elif lst[0] < slst[0]  and ((slst[0] != 9) and (lst[0] != 0)):
        slst.append(lst[0])
        slst.append(slst[0])
    elif (lst[0] == 9) and (slst[0] == 0):
        slst.append(lst[0])
        slst.append(slst[0])
    elif (slst[0] == 0) and (lst[0] == 9):
        lst.append(slst[0])
        lst.append(lst[0])
    lst.pop(0)
    slst.pop(0) 
    count += 1
    if len(lst) == 0:
        print('second', end=' ', file = fout)
        print(count, file = fout)
        y = 1
        break
    if len(slst) == 0:
        print('first', end=' ', file = fout)
        print(count, file = fout)
        y = 1
        break
if y == 0:
    print('draw', file = fout)

fin.close()
fout.close()