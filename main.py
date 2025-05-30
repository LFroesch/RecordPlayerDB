from graphics import Window
import sys
import shared
import time
import records

def main():
    win = Window(shared.screen_x, shared.screen_y)
    win.reset_list()
    #canvas = win.get_canvas() # dont need atm
    root = win.get_root()
    title = win.get_title()
    print(f"Launching {title}")

    # leave at end
    win.run()

if __name__ == "__main__":
    main()