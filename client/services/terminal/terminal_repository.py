import curses


class TerminalRepository:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        curses.start_color()
        curses.use_default_colors()
        self.stdscr.keypad(True)
    
    @property
    def height(self):
        return self.get_terminal_size()[0]
    
    @property
    def width(self):
        return self.get_terminal_size()[1]
    
    @property
    def x(self):
        return self.stdscr.getyx()[1]
    
    @property
    def y(self):
        return self.stdscr.getyx()[0]

    def get_terminal_size(self):
        return self.stdscr.getmaxyx()

    def clear_terminal(self):
        self.stdscr.clear()

    def start_color(self, color_pair):
        self.stdscr.attron(curses.color_pair(color_pair))

    def end_color(self, color_pair):
        self.stdscr.attroff(curses.color_pair(color_pair))

    def addstr_color(self, y, x, str, color_pair):
        self.stdscr.attron(curses.color_pair(color_pair))
        self.stdscr.addstr(y, x, str)
        self.stdscr.attroff(curses.color_pair(color_pair))

    def start_style(self, style):
        self.stdscr.attron(style)

    def end_style(self, style):
        self.stdscr.attroff(style)

    def addstr(self, y, x, string: str):
        if len(string) >= self.width - x - 1:
            string = string[:self.width - x - 1]
        self.stdscr.addstr(y, x, string)

    def refresh(self):
        self.stdscr.refresh()

    def getch(self):
        return self.stdscr.getch()

    def endwin(self):
        curses.endwin()

    def move(self, y, x):
        self.stdscr.move(y, x)