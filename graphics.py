from tkinter import Tk, BOTH, Canvas, NW
import records
import tkinter as tk
import os
import shared
import sys
import time
import tkinter.ttk as ttk
from PIL import ImageTk, Image

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title('"Record Player DataBase"')
        self.__root.geometry(f"{width}x{height}+1920+0")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.width = width
        self.height = height

        self.__setup_main_window()

    def create_reset_button(self):
        self.reset_button = tk.Button(self.__root, text="Reset", command=self.reset_list)
        self.reset_button.pack()

    def create_search_frame(self):
        search_frame = tk.Frame(self.__root)
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(search_frame, text="Search", command=self.perform_search)
        search_button.pack(side=tk.LEFT)

    def create_results_listbox(self):
        self.results_listbox = tk.Listbox(self.__root, width=50)
        self.results_listbox.pack(pady=10)

    def perform_search(self):
        search_term = self.search_entry.get()
        results = records.search_records(records.records, search_term)
        # Clear Previous Results
        self.results_listbox.delete(0, tk.END)
        if results:
            for result in results:
                artist = result["Artist"]
                record = result["Record"]
                display_string = f"{artist} | {record}"
                self.results_listbox.insert(tk.END, display_string)
        else:
            self.results_listbox.insert(tk.END, "No Results Found")

    def perform_add(self):
        artist = self.__artist_entry.get()
        record = self.__record_entry.get()
        if artist and record:
            result = records.add_to_records(records.records, artist, record)
            if result:  # Assuming add_to_records returns True on success
                print(f"Successfully added {artist} - {record} to the database")
            else:
                print("Failed to add record to the database")
        else:
            print("Artist and record name cannot be empty")

    def close(self):
        self.__running = False
        self.__root.destroy()
        print("Window Closed")

    def run(self):
        self.__root.mainloop()

    def get_title(self):
        return self.__root.title()

    def get_canvas(self):
        return self.__canvas
    
    def get_root(self):
        return self.__root
    
    def reset_list(self):
        self.results_listbox.delete(0, tk.END)  # Clear the listbox
        for record in records.records:  # Assuming self.records contains all records
        # Insert each record into the listbox
            self.results_listbox.insert(tk.END, f"{record['Artist']} - {record['Record']}")
    
    def show_add_record_window(self):
        # Clear existing widgets
        for widget in self.__root.winfo_children():
            widget.destroy()

        # Create new widgets for adding a record
        artist_label = tk.Label(self.__root, text="Artist:")
        artist_label.pack()
        self.__artist_entry = tk.Entry(self.__root)
        self.__artist_entry.pack()

        record_label = tk.Label(self.__root, text="Record:")
        record_label.pack()
        self.__record_entry = tk.Entry(self.__root)
        self.__record_entry.pack()

        add_button = tk.Button(self.__root, text="Add Record", command=self.perform_add)
        add_button.pack()

        back_button = tk.Button(self.__root, text="Back to Main", command=self.__setup_main_window)
        back_button.pack()

    def __setup_main_window(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

        self.create_search_frame()
        self.create_results_listbox()
        self.create_reset_button()
        back_button = tk.Button(self.__root, text="To Add GUI", command=self.show_add_record_window)
        back_button.pack()

        self.__canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        self.reset_list()