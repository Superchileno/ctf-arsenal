import sys
out=[]
def add(*xs): out.extend(str(x) for x in xs)
# 1) build cars with assorted model/team/driver/engine lengths
lens = [0,1,2,3,4,7,8,9,10,11,12,13,15,16,17,24,25,26,28,29,31,32,33,48,49,50,52,56,57,64,72,73,80,89,90,92,96,100,200,500,1023]
for L in lens:
    add(1, 'M'*L, 'T'*L, 'D'*L, 'E'*L, '50', '1m2s', '10','20','30','40','50')
# 2) tune each car, all fields, with boundary lengths and '-'
for i in range(1, len(lens)+1):
    add(4, i)
    add('M'*min(1023, (i*7) % 200 + 1), 'T'*((i*13) % 100 + 1), 'D'*((i*17) % 50 + 1), 'E'*((i*19) % 30 + 1))
    add('400', '999999999m59s', '255','1','0','255','1')
# 3) show garage all sorts/directions
for s in range(0,7):
    for d in (1,2):
        add(3, s, d)
# 4) scrap some
for i in range(1, len(lens)+1, 3):
    add(2, i)
add(5)
sys.stdout.write('\n'.join(out)+'\n')
