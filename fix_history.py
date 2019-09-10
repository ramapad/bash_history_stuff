
# Going to use this file to read in a list of .bash_history_bkups file and use that to create a new consolidated .bash_history

# (i) On rain: ls -la | grep "\.bash_history" | awk '{print $9}' | grep -v "umd_mac" > list_of_bash_history_bkups
# (i) On swirl: ls -d ~/bash_history_bkups/* > list_of_bash_history_bkups

# (ii) python fix_history.py .bash_history_consolidated_jan_03_2018
# (iii) cp .bash_history_consolidated_jan_03_2018 .bash_history

import sys
import collections
from operator import *
import datetime

files_ls = []
# Read the list of .bash_history_bkups from a file called 'list_of_bash_history_bkups'
list_fp = open('list_of_bash_history_bkups', 'r')
for line in list_fp:
    files_ls.append(line[:-1])

hist_line = collections.namedtuple('hist_line', 'ts cmd')

hist_lines = []
ts_to_cmds = {}

file_num = 0

for fname in files_ls:
    file_num += 1

    # sys.stdout.write("Processing {0}\n".format(fname) )
    if file_num%1000 == 0:
        sys.stdout.write("{0} files processed at {1}\n".format(file_num, str(datetime.datetime.now() ) ) )

    fp = open(fname, 'r')
    line_num = 0
    prev_line = ''
    for line in fp:
        line_num += 1
        if (line[:1] == '#'):
            ts = line[1:-1]
            prev_line = 'ts'
        else:
            if (prev_line == 'ts'):
                cmd = line[:-1]
                if ts not in ts_to_cmds:
                    ts_to_cmds[ts] = []
                    new_hist_line = hist_line(ts=ts, cmd=cmd)
                    hist_lines.append(new_hist_line)
                    ts_to_cmds[ts].append(cmd)
                else:
                    # ts is in ts_to_cmds, so we've seen this ts before. Some times a new command is associated with the same ts if I typed commands too close to each other. At other times, we have duplicates: the same command is associated with the same timestamp. Discard the duplicates, keep the non-duplicates.
                    if (cmd not in ts_to_cmds[ts]):
                        new_hist_line = hist_line(ts=ts, cmd=cmd)
                        hist_lines.append(new_hist_line)
                        ts_to_cmds[ts].append(cmd)
                    else:
                        pass

            elif (line_num > 1):
                # I could optionally chose to drop lines which are not preceded by a timestamp but why not include them?
                new_hist_line = hist_line(ts=ts, cmd=line[:-1])
                hist_lines.append(new_hist_line)
                # print fname
                # print line_num
                # print line
                pass
                # sys.exit(1)
            else:
                pass # line_num == 1 and ts hasn't been initialized yet

            prev_line = 'cmd'
    
sorted_hist_lines = sorted(hist_lines, key=attrgetter('ts'))        
    
op_fp = open(sys.argv[1], 'w')
for entry in sorted_hist_lines:
    op_fp.write('#{0}\n'.format(entry.ts))
    op_fp.write('{0}\n'.format(entry.cmd))
