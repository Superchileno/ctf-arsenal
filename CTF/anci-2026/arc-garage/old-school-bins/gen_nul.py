import sys
lines = []
lines += ['1', 'AAAAAAAAAA', '', '', '', '', '', '', '', '', '', '']   # build -> car #5
lines += ['4', '5']                                                    # tune car 5
lines += [b'BB\x00CCCC'.decode('latin1')]                              # model with embedded NUL
lines += ['', '', '', '', '', '', '', '', '', '']                      # rest of tune fields
lines += ['3', '0', '1']
lines += ['5']
sys.stdout.buffer.write(('\n'.join(lines) + '\n').encode('latin1'))
