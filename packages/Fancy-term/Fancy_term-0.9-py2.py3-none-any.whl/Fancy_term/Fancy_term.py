# -*- coding: utf-8 -*-

# <-------------- colors --------------> #


class _colors:
    def __init__(self):
        self._beginning = "\033["
        self.red = "31;10m"
        self.white = "31;97m"
        self.green = "32;400m"
        self.yellow = "33;40m"
        self.purple = "34;40m"
        self.rose = "35;40m"
        self.blue = "36;36m"
        self.reset = self._beginning + self.white
        self.end = "\033[m"


colors = _colors()

Colors_available = ["red", "white", "green",
                    "yellow", "purple", "rose", "blue", "reset"]
Substyles_available = ["bold", "faded", "less_faded",
                       "underligned", "blinking", "background", "normal"]
# <-------------- colors --------------> #


def printc(style, *strings, sep=''):
    print(style.str(), sep.join(strings), colors.end, sep="")


def colored_string(style, *strings, sep=''):
    return style.str() + sep.join(strings) + colors.end


class Smart_print:
    """
            Can be used to set a style or directly used as a print function
    """

    def __init__(self, *args, **kwargs):
        self.default_style = Style(color=colors.white)
        self.actual_style = kwargs.get('style', self.default_style)
        self.prefix = kwargs.get('prefix', '')
        self.suffix = kwargs.get('suffix', '')

        self.up = '\x1b[1A'
        self._reset = colors.reset
        self.end = "\033[m"

    def set(self, style=None):
        """
                Sets a Style for future use : Should work with any printable stuff
        """
        if style != None:
            print(self.up, style(), sep="")
            self.actual_style = style
        else:
            if self.actual_style != None:
                print(self.end, self.actual_style.str(), self.up, sep='')
            else:
                print("no style defined")

    def use(self, style):
        self.actual_style = style

    def reset(self):
        print(self.up, self._reset, sep="")
        self.actual_style = None

    def __call__(self, *strings):
        try:
            print(self.prefix, self.end, self.actual_style.str(),
                  ''.join(strings), self.end, self.suffix, sep="")
        except:
            raise Exception("no style defined")


class Style:
    """
            Colors    available by typing print(Colors_available)
            Substyles available by typing print(Substyles_available)
    """

    def __init__(self, *args, **kwargs):
        self._sub_styles = {"bold": "1", "faded": "2", "less_faded": "3",
                            "underligned": "4", "blinking": "5", "background": "7", "normal": "0"}
        self._beginning = "\033["
        self.default = 'normal'
        self.bold = kwargs.get(self.default, True)
        self._color = kwargs.get('color', colors.red)
        self._sub_style = self._sub_styles.get(
            kwargs.get('substyle', self.default))
        self._gen_substyle(kwargs.get('substyle', self.default))
        self.end = "\033[m"

    def str(self):
        return(self.end + self._beginning + self._sub_style + self._color)

    def __call__(self):
        return(self.end + self._beginning + self._sub_style + self._color)

    def __str__(self):
        return(self.end + self._beginning + self._sub_style + self._color)

    def __repr__(self):
        return(self._beginning[1:] + self._sub_style + self._color)

    def _gen_substyle(self, sub_styles):
        styles = sub_styles.split(",")
        L_styles = []
        self._sub_style = ""
        for style in styles:
            try:
                L_styles.append(int(self._sub_styles[style]))
            except:
                print(str(style), "not a valid format")
        L_styles.sort()
        for i in L_styles:
            self._sub_style += str(i) + ";"


# <-------------- test unit --------------> #
if __name__ == '__main__':
    suc = Style(color=colors.green, substyle='bold')
    a = colored_string(suc, 'success', sep=" ")
    sucess_printer = Smart_print(prefix='['+a+'] ')
    sucess_printer('test')
# <-------------- test unit --------------> #
