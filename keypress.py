import time
from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()
def on_press(key):
    if not key in [Key.scroll_lock, Key.alt_l, Key.ctrl_l, Key.tab, Key.esc]:
        keyboard.press(Key.scroll_lock)
        keyboard.release(Key.scroll_lock)
    # print(key, type(key))

def on_release(key):
    pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# while True:
#     time.sleep(2.5)
#     keyboard.press(Key.right)