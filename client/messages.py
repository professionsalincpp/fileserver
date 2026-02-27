import re
from tabulate import tabulate
from model.statuscodes import CommandStatusCode


def print_table(data: list, adjust_width: bool=True) -> None:
    width: int = 50
    table_rows: int = len(data)
    table_columns: int = len(data[0])
    column_widths = []
    if adjust_width:
        for column in range(table_columns):
            column_width = 0
            for row in range(table_rows):
                if len(data[row][column]) - get_ansi_escapes_count(data[row][column]) + 2 > column_width:
                    column_width = len(data[row][column]) - get_ansi_escapes_count(data[row][column]) + 4
            column_widths.append(column_width)
        column_width = max(column_widths)
    else:
        column_width = width // table_columns
        for column in range(table_columns):
            column_widths.append(column_width)
    width = max(sum(column_widths), width)
    last_cell_pos_x = 0
    column = 0
    print("╭", end="")
    for i in range(width):
        if (last_cell_pos_x + column_widths[column] + 1) == i and column < table_columns - 1:
            print("┬", end="")
            column += 1
            last_cell_pos_x = i
        else:
            print("─", end="")
    print("╮")
    for row in range(table_rows):
        print("│ ", end="")
        last_cell_pos_x = 0
        for column in range(table_columns):
            cell = data[row][column]
            column_width = column_widths[column]
            if len(cell) - get_ansi_escapes_count(cell) > column_width:
                cell = cell[:column_width - 4] + "..."
            if column != len(data[row]) - 1:
                cell += " " * (get_dist_to_frame_end(cell, column_width)) + "│ "
            else:
                cell += " " * (get_dist_to_frame_end(cell, width - last_cell_pos_x - 1)) + "│"
            last_cell_pos_x += len(cell)
            print(cell, end="")
        print()
        if row == table_rows - 1:
            continue
        last_cell_pos_x = 0
        column = 0
        print("├", end="")
        for i in range(width):
            if (last_cell_pos_x + column_widths[column] + 1) == i and column < table_columns - 1:
                print("┼", end="")
                column += 1
                last_cell_pos_x = i
            else:
                print("─", end="")
        print("┤")
    last_cell_pos_x = 0
    column = 0
    print("╰", end="")
    for i in range(width):
        if (last_cell_pos_x + column_widths[column] + 1) == i and column < table_columns - 1:
            print("┴", end="")
            column += 1
            last_cell_pos_x = i
        else:
            print("─", end="")
    print("╯")


def get_dist_to_frame_end(text: str, frame_width: int=50) -> int:
    return frame_width - len(text) + get_ansi_escapes_count(text)

def get_ansi_escapes_count(text: str) -> int:
    if not text:
        return 0
    else:
        matches: list = re.findall(r'\x1b[^m]*m', text)
        count: int = 0
        for match in matches:
            count += len(match)
        return count
    
def format_server_status(status) -> str:
    circle: str = "●"
    if CommandStatusCode.is_ok(status):
        return f"\033[1;32m{circle}\033[0m {status}"
    else:
        return f"\033[1;31m{circle}\033[0m {status}"
    