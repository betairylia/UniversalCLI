from CLI import CLI
from Components import *

temp = "A.jpg"
a = ProgressBar(tot=20, title = "RANDOM bar", info = lambda cur, tot: '%6.2f - %5s' % (cur / tot * 100.0, temp))
b = CLIComponent(align = 'center')
CLI.init([[a], [b]])
for j in range(20):
    CLI.cnt = j
    a.updateProgressInc(1)
    b.setContent("%3d" % j, 3)
    temp = "%d.jpg" % j
    CLI.update()
    CLI.render()
    # if j == 8:
    #     print("HAHAHAHAHA\nRandom output from random package\nHate them")
    if j % 2 == 0:
        CLI.log("Loss = MAGIC")
        # sleep(1)
