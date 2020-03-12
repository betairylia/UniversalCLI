import math
from termcolor import colored

class CLIComponent:

    def __init__(self, chwidth = 80, align = 'left', padchar = ' '):
        self.chwidth = chwidth
        self.align = align
        self.padchar = padchar

        self.content = 'EMPTY COMPONENT'
        self.lenth = len(self.content)

    def setContent(self, content, lenth):
        self.content = content
        self.lenth = lenth

    def render(self):
        return self.content, self.lenth

    def __repr__(self):
        
        string, strlen = self.render()
        pad = [0, 0]
        
        if self.align == 'left':
            # string = string[:self.chwidth]
            # strlen = len(string)
            pad[1] = self.chwidth - strlen

        elif self.align == 'right':
            # string = string[-self.chwidth:]
            # strlen = len(string)
            pad[0] = self.chwidth - strlen

        elif self.align == 'center':
            # string = string[-((self.chwidth + strlen) // 2):math.ceil((self.chwidth + strlen) / 2)]
            # strlen = len(string)
            pad[0] = (self.chwidth - strlen) // 2
            pad[1] = self.chwidth - strlen - pad[0]

        else:
            print("CLI: Alignment not supported")
            raise NotImplementedError

        return "%s%s%s" % (self.padchar * pad[0], string, self.padchar * pad[1]) 

class ProgressBar(CLIComponent):

    def __init__(
        self, chwidth = 80, 
        cur = 0, tot = 100,
        left = '<', right = '>', fill = '=', empty = ' ',
        borderstyle = (None, None, None), 
        fillstyle = (None, None, None),
        emptystyle = (None, None, None),
        titlestyle = (None, None, None), 
        infostyle = (None, None, None), 
        # numberstyle = (None, None, None), 
        title = 'Bar',
        info = lambda cur, tot: '%3d / %3d' % (cur, tot)):

        super().__init__(chwidth, 'center')
        self.cur = cur
        self.tot = tot
        self.charset = [left, right, fill, empty]
        self.style = [borderstyle, fillstyle, emptystyle, titlestyle, infostyle]
        self.title = title
        self.info_foo = info
    
    def updateProgress(self, cur):
        self.cur = cur
    
    def updateProgressInc(self, increment = 1):
        self.cur += increment

    def render(self):
        
        # alias
        bs, fs, es, ts, ins = self.style
        l, r, f, e = self.charset
        
        # Get info and title
        info_str = self.info_foo(self.cur, self.tot)
        title = self.title
        
        # Calculate lenth for fills
        barwid = self.chwidth - len(title) - 5 - len(info_str)
        per = self.cur / self.tot
        fill = int(per * barwid)
        fill = [fill, barwid - fill]

        # Render string
        final = "%s: %s %s%s%s%s" % (colored(title, *ts), colored(info_str, *ins), colored(l, *bs), colored(f * fill[0], *fs), colored(e * fill[1], *es), colored(r, *bs))
        return final, self.chwidth
