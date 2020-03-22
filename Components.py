import warnings
import sys
import math
import io
from termcolor import colored
from contextlib import redirect_stdout


class CLIComponent:

    def __init__(self, chwidth = 80, align = 'left', padchar = ' '):
        self.chwidth = chwidth
        self.align = align
        self.padchar = padchar

        self.content = 'EMPTY COMPONENT'
        self.lenth = len(self.content)

        self.pCLI = None
        self.refresh()

    def setContent(self, content, lenth = None):
        self.content = content
        self.lenth = lenth or len(content)
        self.refresh()

    def render(self):
        return self.content, self.lenth

    def refresh(self):
        if self.pCLI is not None:
            self.pCLI.updateRender()

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

class Styled(CLIComponent):

    def __init__(self, chwidth = 80, align = 'left', padchar = ' ', style = (None, None, None)):
        super().__init__(chwidth, align, padchar)
        self.style = style
        self.refresh()

    def setContent(self, content):
        self.content = colored(content, *self.style)
        self.lenth = len(content)
        self.refresh()

    def __call__(self, content):
        self.setContent(content)

class ProgressBar(CLIComponent):

    def __init__(
        self, chwidth = 80, 
        cur = 0, tot = 100,
        left = '<', right = '>', fill = '=', empty = ' ',
        preset = None,
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

        self.presets = {'classic': ['<', '>', '=', ' '], 
                        'rect': ['|', '|', '\u25A7', '\u25A1'], 
                        'shades': ['|', '|', '\u2588', '\u2591'],
                        'magic': ['|', '|', '\u2605', '\u2606'],
                        'wtf': ['|', '|', '\u5B8C', '\u2F0D'],
                        'wtf2': ['|', '|', '\u3048', '\u3047'],
                        'wtf3': ['[', ']', '\u70EB', '  ']}
        if preset is not None and preset in self.presets:
            self.charset = self.presets[preset]
            if preset.startswith('wtf'):
                self.chwidth = int(self.chwidth / 1.45)
        else:
            self.charset = [left, right, fill, empty]

        self.style = [borderstyle, fillstyle, emptystyle, titlestyle, infostyle]
        self.title = title
        self.info_foo = info
        self.refresh()
    
    def updateProgress(self, cur):
        self.cur = cur
        self.refresh()
    
    def updateProgressInc(self, increment = 1):
        self.cur += increment
        self.refresh()

    def reset(self):
        self.cur = 0
        self.refresh()

    def __call__(self, cur, tot, title = None, info = None):
        self.cur = cur
        self.tot = tot
        if title: self.title = title
        if info:  self.info_foo = info
        self.refresh()

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

class RedirectWrapper(object):
    def __init__(self, target_cli=None):
        self.CLI = target_cli

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            f = io.StringIO()
            with redirect_stdout(f), warnings.catch_warnings(record=True) as w:
                # wrapped func
                re = func(*args, **kwargs)
                # sleep(1)
            try:
                while(len(w) != 0):
                    self.CLI.log('[Warning] ' + warnings._formatwarnmsg_impl(w.pop(0))[:-1])
                if(f.getvalue() != ''):
                    lines = f.getvalue().splitlines()
                    for line in lines:
                        self.CLI.log('[Output] ' + line)
            except AttributeError:
                print('CLI does not exist.')
            return re
        return wrapper