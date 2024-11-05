from pynput.keyboard import Key

keys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'space', 'enter', 'tab', 'backspace', 'delete', 'esc',
    'shift', 'shift_r', 'ctrl', 'ctrl_r', 'alt', 'alt_r',
    'caps_lock', 'cmd', 'cmd_r', 'f1', 'f2', 'f3', 'f4',
    'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'home', 'end', 'page_up', 'page_down', 'left', 'right',
    'up', 'down', 'insert', 'menu', 'pause', 'print_screen',
    'scroll_lock', 'num_lock'
]

key_mapping = {
    'space': Key.space, 'enter': Key.enter, 'tab': Key.tab, 'backspace': Key.backspace, 'delete': Key.delete, 'esc': Key.esc,
    'shift': Key.shift, 'shift_r': Key.shift_r, 'ctrl': Key.ctrl, 'ctrl_r': Key.ctrl_r, 'alt': Key.alt, 'alt_r': Key.alt_r,
    'caps_lock': Key.caps_lock, 'cmd': Key.cmd, 'cmd_r': Key.cmd_r, 'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
    'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8, 'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
    'home': Key.home, 'end': Key.end, 'page_up': Key.page_up, 'page_down': Key.page_down, 'left': Key.left, 'right': Key.right,
    'up': Key.up, 'down': Key.down, 'insert': Key.insert, 'menu': Key.menu, 'pause': Key.pause, 'print_screen': Key.print_screen,
    'scroll_lock': Key.scroll_lock, 'num_lock': Key.num_lock
}