import sys
# Build 12 cars with 90-char model and team -> many class-5 chunks (struct+string)
n = 12
m = 90
out = []
for i in range(n):
    model = ('M%03d' % i).ljust(m-1, 'A')
    team  = ('T%03d' % i).ljust(m-1, 'B')
    out += ['1', model, team, '', '', '100', '', '', '', '', '', '']
out += ['3', '0', '1', '5']
sys.stdout.write('\n'.join(out) + '\n')
