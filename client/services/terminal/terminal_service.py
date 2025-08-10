
import sys
from services.terminal.terminal_repository import TerminalRepository
import curses


class TerminalService(TerminalRepository):
    def __init__(self):
        super().__init__()
        curses.init_color(8, 700, 700, 700)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, 8, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.init_keys()

    def init_keys(self) -> None:
        if sys.platform == 'win32':
            self.contol_s_code = 19
            self.contol_z_code = 26
            self.delete_code = 127
        elif sys.platform == 'darwin':  # macOS
            if 'ITERM' in os.environ.get('TERM_PROGRAM', ''):
                self.contol_s_code = 22
                self.contol_z_code = 26
                self.delete_code = 127
            elif 'XTERM' in os.environ.get('TERM', '') or 'RXVT' in os.environ.get('TERM', ''):
                self.contol_s_code = 22
                self.contol_z_code = 26
                self.delete_code = 330
            else:
                self.contol_s_code = 19
                self.contol_z_code = 26
                self.delete_code = 127
        elif sys.platform == 'linux':
            if 'GNOME' in os.environ.get('TERM', '') or 'KDE' in os.environ.get('TERM', ''):
                self.contol_s_code = 22
                self.contol_z_code = 26
                self.delete_code = 127
            else:
                self.contol_s_code = 19
                self.contol_z_code = 26
                self.delete_code = 127

    @property
    def contol_s(self):
        if not hasattr(self, 'contol_s_code'):
            self.init_keys()
        return self.contol_s_code
    
    @property
    def contol_z(self):
        if not hasattr(self, 'contol_z_code'):
            self.init_keys()
        return self.contol_z_code
    
    @property
    def delete(self):
        if not hasattr(self, 'delete_code'):
            self.init_keys()
        return self.delete_code        

    def draw_top_str(self, string: str) -> None:
        if self.width < 3:
            return
        if len(string) > self.width:
            string = string[:self.width-3]
            string += "..."
        string = f"{string:<{self.width}}"
        self.start_color(3)
        self.addstr(0, 0, string)
        self.end_color(3)

    def draw_top_panel(self, title: str, message: str) -> None:
        top_str = f"{title} | {message}"
        self.draw_top_str(top_str)

    def addscrollstr(self, y: int, x: int, scroll: int, string: str) -> None:
        string = string[min(scroll, len(string)):]
        self.addstr(y, x, string)