from time import sleep
import curses
from services.file_system.file_system_service import FileSystemService
from services.terminal.terminal_service import TerminalService
from services.file_system.file_dialog import FileDialog



class FileViewer:
    def __init__(self, data: str, readonly: bool = False):
        self.file_path = data
        self.file_system_service = FileSystemService()
        try:
            self.file_contents = self.file_system_service.read_file().split("\n")
        except:
            self.file_contents = data.split("\n")
        self.current_line = 1
        self.terminal_service = TerminalService()
        self.cursor_position = 0
        self.running = True
        self.readonly = readonly
        self.scroll_x = 0

    @property
    def text_width(self):
        if self.terminal_service.width > 10:
            return self.terminal_service.width - 10
        else:
            return 10
        
    @property
    def current_line_text(self):
        return self.file_contents[self.current_line]


    def redraw(self):
        # print("\033[2J\033[H")
        # os.system("cls" if os.name == "nt" else "clear")
        # remove_text_from_terminal(self.get_file_contents())

        contents = self.get_file_contents()
        start_line = max(0, self.current_line - self.terminal_service.height // 2)
        current_line = contents[self.current_line - start_line]
        self.scroll_x = 0
        new_cursor_position = self.cursor_position
        if new_cursor_position >= len(current_line) - 1:
            new_cursor_position = max(0, len(current_line) - 1)
        elif new_cursor_position < 0:
            new_cursor_position = 0
        if new_cursor_position >= self.terminal_service.width - 9:
            self.scroll_x = new_cursor_position - self.terminal_service.width + 10
            new_cursor_position = self.terminal_service.width - 10
        self.terminal_service.clear_terminal()
        self.terminal_service.start_color(3)
        topstr = f"Save(s-{str(self.terminal_service.contol_s)}) Quit(Esc) Len {len(self.current_line_text)} Pos {self.cursor_position} "
        self.terminal_service.draw_top_panel(f"File Viewer: ", topstr)
        self.terminal_service.end_color(3)
                
        for i, line in enumerate(contents):
        
            # create a number for the line
            if i + start_line == self.current_line:
                self.terminal_service.start_color(7)  # красный цвет
            else:
                self.terminal_service.start_color(2)  # серый цвет и курсив
            self.terminal_service.addstr(i+1, 0, f"{i+1+start_line:>4} ")
            self.terminal_service.addstr(i+1, 5, " │ ")
            self.terminal_service.end_color(7)  # вернуть цвет
            self.terminal_service.end_color(2)
            try:
                self.terminal_service.addscrollstr(i+1, 8, self.scroll_x, line)
            except:
                self.terminal_service.draw_top_str(f"Error: L: {self.current_line} C: {self.cursor_position} S: {self.scroll_x} T: {self.text_width}")
        if self.scroll_x == 0:
            self.terminal_service.move(self.current_line - start_line + 1, 8 + new_cursor_position)
        else:
            self.terminal_service.move(self.current_line - start_line + 1, 8 + self.text_width - 1)                                                                      
        self.terminal_service.refresh()

    def save_file(self):
        filename = FileDialog().run()
        if filename == "cancel":
            return
        self.file_system_service.save_file(filename, ''.join(self.file_contents))
        self.terminal_service.clear_terminal()
        self.terminal_service.draw_top_panel("File Viewer: ", f"Saved to {filename}")
        self.terminal_service.refresh()
        sleep(2)
        

    def move_left(self):
        if self.cursor_position > len(self.file_contents[self.current_line]) - 1:
            self.cursor_position = len(self.file_contents[self.current_line]) - 1
        if self.cursor_position > 0:
            self.cursor_position -= 1
        elif self.current_line > 0:
            self.current_line -= 1
            self.cursor_position = len(self.file_contents[self.current_line]) - 1
        self.redraw()

    def move_right(self):
        if self.cursor_position < len(self.file_contents[self.current_line]) - 1:
            self.cursor_position += 1
        else:
            if self.current_line < len(self.file_contents) - 1:
                self.current_line += 1
                self.cursor_position = 0
        self.redraw()

    def get_file_contents(self):
        start_line = max(0, self.current_line - self.terminal_service.height // 2)
        if self.current_line > len(self.file_contents) - self.terminal_service.height // 2:
            end_line = len(self.file_contents) + 2
        elif self.current_line >= self.terminal_service.height // 2:
            end_line = min(len(self.file_contents), self.current_line + self.terminal_service.height // 2 + 1)
        else:
            end_line = self.current_line + self.terminal_service.height // 2 + (self.terminal_service.height // 2 - self.current_line)
        end_line = max(0, end_line - 2) # Adjust end_line to be exclusive
        lines = []
        for i, line in enumerate(self.file_contents[start_line:end_line]):
            lines.append(line)
        return lines

    def move_up(self):
        if self.current_line > 0:
            self.current_line -= 1
        self.redraw()

    def move_down(self):
        if self.current_line < len(self.file_contents) - 1:
            self.current_line += 1
        self.redraw()

    def add_char(self, char):
        if char == '\n' or char == '\r':
            text_before = self.file_contents[self.current_line][:self.cursor_position]
            text_after = self.file_contents[self.current_line][self.cursor_position:]
            self.file_contents[self.current_line] = text_before
            self.file_contents.insert(self.current_line + 1, text_after)
            self.current_line += 1
            self.cursor_position -= len(text_before)
            self.redraw()
            return
        self.file_contents[self.current_line] = \
            self.file_contents[self.current_line][:self.cursor_position] + char + self.file_contents[self.current_line][self.cursor_position:]
        self.cursor_position += 1
        self.redraw()

    def backspace_char(self):
        abs_position = min(self.cursor_position, len(self.file_contents[self.current_line]))
        if abs_position > 0:
            self.file_contents[self.current_line] = \
                self.file_contents[self.current_line][:abs_position - 1] + self.file_contents[self.current_line][abs_position:]
            self.cursor_position -= 1
        else:
            if self.current_line > 0:
                text_before = self.file_contents[self.current_line - 1]
                text_after = self.file_contents[self.current_line]
                self.file_contents[self.current_line - 1] += text_after
                self.file_contents = self.file_contents[:self.current_line] + self.file_contents[self.current_line + 1:]
                self.current_line -= 1
                self.cursor_position = len(text_before)
                
        self.redraw()

    def delete_char(self):
        if self.cursor_position < len(self.file_contents[self.current_line]):
            self.file_contents[self.current_line] = \
                self.file_contents[self.current_line][:self.cursor_position] + self.file_contents[self.current_line][self.cursor_position + 1:]
        self.redraw()
    

    def run(self):
        self.redraw()
        while True:
            c = self.terminal_service.getch()
            if c == curses.KEY_RESIZE:
                self.redraw()
            if c == 27:
                break
            if c == self.terminal_service.contol_s:
                self.save_file()
            elif c == curses.KEY_UP:
                self.move_up()
            elif c == curses.KEY_DOWN:
                self.move_down()
            elif c == curses.KEY_LEFT:
                self.move_left()
            elif c == curses.KEY_RIGHT:
                self.move_right()
            elif c == ord('\b'):
                self.backspace_char()
            elif c == ord("Ŋ"):
                self.delete_char()
            else:
                self.add_char(chr(c))
            self.redraw()
        curses.endwin()

