import curses
import os
from services.terminal.terminal_service import TerminalService

class FileDialog:
    def __init__(self):
        self.terminal_service = TerminalService()
        self.current_dir = os.getcwd()
        self.files = [".."]
        self.files.extend(os.listdir(self.current_dir))
        self.selected_file = ""
        self.cursor_pos = 0
        self.entry_cursor_pos = 0
        self.entry_scroll_pos = 0
        self.is_last_entry_touched = False
        self.running = True

    def draw(self):
        self.terminal_service.clear_terminal()
        self.terminal_service.draw_top_panel("File Dialog: ", f"Path: {self.current_dir}")
        start_file = max(0, self.cursor_pos - self.terminal_service.height // 2)
        end_file = min(len(self.files), self.terminal_service.height + start_file - 4)
        for i, file in enumerate(self.files[start_file:end_file]):
            if i == self.cursor_pos - start_file:
                self.terminal_service.start_style(curses.A_REVERSE)
                self.terminal_service.addstr(i + 1, 0, f"{file:<{self.terminal_service.width}}")
                self.terminal_service.end_style(curses.A_REVERSE)
            else:
                self.terminal_service.addstr(i + 1, 0, file)

        self.terminal_service.addstr(self.terminal_service.height - 2, 0, "> ")
        self.terminal_service.addscrollstr(self.terminal_service.height - 2, 2, self.entry_scroll_pos, self.selected_file)
        self.terminal_service.move(self.terminal_service.height - 2, self.entry_cursor_pos + 2)
        self.terminal_service.refresh()

    def move_cursor(self, direction):
        self.is_last_entry_touched = True
        if direction == 1:
            if self.entry_cursor_pos < self.terminal_service.width - 3:
                self.entry_cursor_pos += 1
            elif self.entry_scroll_pos < len(self.selected_file) - self.terminal_service.width + 3:
                self.entry_scroll_pos += 1
        elif direction == -1:
            if self.entry_cursor_pos > 0:
                self.entry_cursor_pos -= 1
            elif self.entry_scroll_pos > 0:
                self.entry_scroll_pos -= 1

    def move_backspace(self):
        if self.entry_scroll_pos > 0:
            self.entry_scroll_pos -= 1
        elif self.entry_cursor_pos > 0:
            self.entry_cursor_pos -= 1

    def handle_input(self):
        ch = self.terminal_service.getch()
        if ch == 27:
            self.running = False
            self.selected_file = "cancel"
        elif ch == curses.KEY_ENTER or ch == ord('\n') or ch == ord('\r'):
            # выбрать файл
            if not os.path.isdir(os.path.join(self.current_dir, self.selected_file)) and self.selected_file != "..":
                self.selected_file = os.path.join(self.current_dir, self.selected_file)
                self.running = False
            elif self.cursor_pos == 0:
                self.current_dir = os.path.dirname(self.current_dir)
                self.files = [".."]
                self.files.extend(os.listdir(self.current_dir))
            else:
                self.current_dir = os.path.join(self.current_dir, self.files[self.cursor_pos])
                self.files = [".."]
                self.files.extend(os.listdir(self.current_dir))
            self.cursor_pos = 0
        elif ch == curses.KEY_UP:
            # навигация вверх
            if self.is_last_entry_touched:
                self.is_last_entry_touched = False
                return
            self.cursor_pos = (self.cursor_pos - 1) if self.cursor_pos > 0 else 0
            self.selected_file = self.files[self.cursor_pos]
            self.entry_cursor_pos = len(self.selected_file)
        elif ch == curses.KEY_DOWN:
            # навигация вниз
            self.cursor_pos = (self.cursor_pos + 1) if self.cursor_pos < len(self.files) - 1 else len(self.files) - 1
            self.selected_file = self.files[self.cursor_pos]
            self.entry_cursor_pos = len(self.selected_file)
        elif ch == curses.KEY_LEFT:
            self.move_cursor(-1)
        elif ch == curses.KEY_RIGHT:
            self.move_cursor(1)
        else:
            # команда cd
            if ch == ord('\b') and (self.entry_cursor_pos > 0 or self.entry_scroll_pos > 0):
                self.selected_file = self.selected_file[:self.entry_cursor_pos - 1+self.entry_scroll_pos] + self.selected_file[self.entry_cursor_pos+self.entry_scroll_pos:]
                self.move_backspace()
            elif ch != ord('\b'):
                self.selected_file = self.selected_file[:self.entry_cursor_pos+self.entry_scroll_pos] + chr(ch) + self.selected_file[self.entry_cursor_pos+self.entry_scroll_pos:]
                self.move_cursor(1)

    def run(self) -> str:
        while self.running:
            self.draw()
            self.handle_input()
        selected_file = self.selected_file
        if os.path.exists(selected_file):
            self.running = True
            while self.running:
                char = self.terminal_service.getch()
                self.terminal_service.clear_terminal()
                self.terminal_service.draw_top_panel("File Dialog: ", f"File exists. Overwrite? (y/n)")
                self.terminal_service.addstr(2, 0, f"Path: {selected_file:<{self.terminal_service.width}}")
                if char == ord('n'):
                    selected_file = "cancel"
                    self.running = False
                elif char == ord('y'):
                    self.running = False
        curses.endwin()
        return selected_file
