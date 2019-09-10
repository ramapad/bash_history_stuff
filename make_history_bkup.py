
import sys
import os

import datetime

curr_time = datetime.datetime.now()

cp_cmd = 'cp .bash_history ./bash_history_bkups/bash_history_bkup_{0}_{1}_{2}_{3}'.format(curr_time.year, curr_time.month, curr_time.day, curr_time.hour)
os.system(cp_cmd)

