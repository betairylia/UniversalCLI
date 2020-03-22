from CLI import CLI
from Components import *

temp = "A.jpg"
a = ProgressBar(tot=20, title = "RANDOM bar", preset='magic', info = lambda cur, tot: '%6.2f - %5s' % (cur / tot * 100.0, temp))
b = CLIComponent(align = 'center')
CLI.init([[a], [b]], borderstyle = ('magenta', None, ['bold']))

@RedirectWrapper(target_cli=CLI)
def foo1(j):
    if(j % 2 == 0):
        print("Loss = MAGIC")
    
    if(j == 8):
        print("HAHAHAHAHA\nRandom output from random package\nHate them")
    
    if(j == 12):
        warnings.warn("A really annoying deprecated warning", DeprecationWarning)
    
    if(j == 15):
        warnings.warn("A not so annoying future warning", FutureWarning)

for j in range(20):
    CLI.cnt = j
    a.updateProgressInc(1)
    b.setContent("%3d" % j, 3)
    temp = "%d.jpg" % j
    CLI.update()
    CLI.render()

    foo1(j)
    