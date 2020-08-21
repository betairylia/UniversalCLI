'''
Usage:
e.g. python HPtuner.py "TheFileYouWantToRun.py PossibleArgument1 arg2" --Parameter1 0.1,1,10,100,1000 --Parameter2 Choice1,Choice2,Choice3

Make sure TheFileYouWantToRun.py outputs results to some file so you can check the results later.
This script does not collect any outcome of "TheFileYouWantToRun.py".
'''

import os
import argparse
import copy

parser = argparse.ArgumentParser()
parser.add_argument('exec', type=str, help="The program file *.py that will be executed.")
parsed, unknown = parser.parse_known_args()

for arg in unknown:
    if arg.startswith(("-", "--")):
        parser.add_argument(arg, type=str)

args = parser.parse_args()

hpgrid = copy.deepcopy(args.__dict__)
hpgrid.pop("exec")
for hp in hpgrid:
    hpgrid[hp] = hpgrid[hp].split(',')

print("\033[1;31mAll possible HPs: " + repr(hpgrid) + "\033[0m")

# Start HPTune
cnt = 0

finish = False
hpstats = {}
options = {}
for key in hpgrid:
    hpstats[key] = 0
    options[key] = hpgrid[key][hpstats[key]]

while not finish:

    # Run expr
    exec_cmd = "python " + args.exec
    for key in options:
        exec_cmd = exec_cmd + " --%s %s" % (key, options[key])
    print("\033[1;33mCurrently running: " + exec_cmd + "\033[0m")
    os.system(exec_cmd)

    # update HP
    finish = True
    for key in hpgrid:
        hpstats[key] += 1
        hpstats[key] = hpstats[key] % len(hpgrid[key])
        if hpstats[key] != 0:
            finish = False
            break

    for key in hpgrid:
        options[key] = hpgrid[key][hpstats[key]]
