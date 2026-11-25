import sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
m = int(sys.argv[2]) if len(sys.argv) > 2 else 90
out = []
for i in range(n):
    model = ('M%03d' % i).ljust(m-1, 'A')
    out += ['1', model, '', '', '', '100', '', '', '', '', '', '']
    # model, team, driver, engine, top, lap, power, handling, braking, accel, nitro
out += ['3', '1', '1', '5']
sys.stdout.write('\n'.join(out) + '\n')
