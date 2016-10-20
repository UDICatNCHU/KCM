"""Time estimating script

This script is used to estimate the run time of other scripts or python code
"""

import timeit

repeat = 10
run_count = 1


def ave(l):
    count = len(l)
    return sum(l) / count


# setup = '''
# import subprocess
# '''
#
# db_task = '''
# subprocess.call(['python3', '???.py', '-t=王建民', '-m=base_term_cor_term'])
# '''
#
# grep_task = '''
# subprocess.call(['python3', '???.py', '-t=王建民'])
# '''
#
# grep_time = ave(timeit.Timer(stmt=grep_task, setup=setup).repeat(repeat=repeat,
#                                                                  number=run_count))
#
# db_time = ave(timeit.Timer(stmt=db_task, setup=setup).repeat(repeat=repeat,
#                                                              number=run_count))
#
# print('In average, it takes {} sec using db'.format(db_time))
# print('In average, it takes {} sec using grep'.format(grep_time))
