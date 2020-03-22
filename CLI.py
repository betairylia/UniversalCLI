import colorama
from termcolor import colored, cprint
from colorama import Cursor, Fore, Back, Style
from time import sleep
from .Components import *
import random
import os

class CLIClass():

    def init(self, components = [], width = 80, title = ' Untitled ', footer = None, borderstyle = ('grey', None, ['bold'])):

        self.components = components
        self.height = len(self.components)
        self.width = width
        self.borderstyle = borderstyle

        self.title = title
        self.footer = footer

        if self.footer is None:
            self.footer = ' UCLI v0.01 ~ ' + (colored("ft. Manaka ", 'cyan') if random.random() > 0.5 else colored("ft. Mira ", 'yellow'))

        self.heightwb = self.height + 2
        self.widthwb = self.width + 4
        self.cnt = 0

        # register pCLI for components
        for line in components:
            for c in line:
                c.pCLI = self

        os.system(r"printf '\033]2;%s\033\'" + "'%s'" % (title))
        print("")

        self.render(self.heightwb + 1) # initialize

    def update(self):
        sleep(0.2)

    def render(self, offset = 0):

        # Border
        cprint("%s%s" % ((Cursor.UP(self.heightwb - offset) if offset <= self.heightwb else ''), '*' + '-' * (self.width + 2) + '*'), *self.borderstyle)
        for i in range(self.height):
            cprint("| %s |" % (' ' * self.width), *self.borderstyle)
        cprint("%s" % ('*' + '-' * (self.width + 2) + '*'), *self.borderstyle)

        print("%s" % Cursor.UP(self.heightwb), end = '')

        # CLI Name
        print("%s" % Cursor.FORWARD(3), end = '')
        print(self.title)

        # for l in range(self.height):
        #     print("%s" % Cursor.FORWARD(), end = '')
        #     print("%d" % self.cnt)
        for line in self.components:
            print("%s" % Cursor.FORWARD(2), end = '')
            for comp in line:
                print(comp, end = '')
            print('')

        # Footer
        print("%s" % Cursor.FORWARD(30), end = '')
        print(self.footer)
        # print("%s" % Cursor.DOWN(), end = '')
    
    def updateRender(self):
        self.update()
        self.render()

    def clear(self, offset = 0):

        print("%s%s" % (Cursor.UP(self.heightwb - offset), (' ' * self.widthwb + '\n') * self.heightwb))
        print("%s" % (Cursor.UP(self.heightwb - offset + 1)), end = '')

    def trail(self, offset = 0):
        
        self.clear(offset)
        print('Trail')
        self.render(self.heightwb + 1)

    def log(self, string, offset = 0):

        self.clear(offset)
        print(string)
        self.render(self.heightwb + 1)

CLI = CLIClass()

if __name__ == '__main__':

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
            CLI.trail()
            # sleep(1)
