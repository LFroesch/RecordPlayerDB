from graphics import Window
import sys
import shared
import time
import records

def main():
    win = Window(shared.screen_x, shared.screen_y)
    win.reset_list()
    #canvas = win.get_canvas()
    root = win.get_root()
    title = win.get_title()
    print(f"Launching {title}")
    # fix enter to work for 2 different buttons depending on adding state or not
    # win.search_entry.bind('<Return>', lambda event: win.perform_search())

    # leave at end
    win.run()

if __name__ == "__main__":
    main()