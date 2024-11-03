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
        self.reset_button = tk.Button(self.__root, text="Reset", font=("Arial", 14), command=self.reset_list)
        self.reset_button.pack()

    def create_search_frame(self):
        search_frame = tk.Frame(self.__root)
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 14))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(search_frame, text="Search", font=("Arial", 14), command=self.perform_search, height=1)
        search_button.pack(side=tk.LEFT)

    def create_results_listbox(self):
        self.results_listbox = tk.Listbox(self.__root, width=50, font=("Arial", 12))
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
            if result == True:  # Assuming add_to_records returns True on success
                print("-------------------")
                print("Successfully added:")
                print(f"Artist: {artist}")
                print(f"Record: {record}")
                print("to the database")
                print("-------------------")
                records.records = records.load_records()
            else:
                print("Failed to add record to the database")
        else:
            print("Artist and record name cannot be empty")

    def perform_del(self):
        artist = self.__artist_entry.get()
        record = self.__record_entry.get()
        if artist and record:
            result = records.del_from_records(records.records, artist, record)
            if result == True:  # Assuming add_to_records returns True on success
                print("-------------------")
                print("Successfully deleted:")
                print(f"Artist: {artist}")
                print(f"Record: {record}")
                print("from the database")
                print("-------------------")
            else:
                print("Failed to delete record to the database")
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
            if isinstance(record, list):
            # Assuming the list is in [Artist, Record] format
                self.results_listbox.insert(tk.END, f"{record[0]} - {record[1]}")
            elif isinstance(record, dict):
                self.results_listbox.insert(tk.END, f"{record['Artist']} - {record['Record']}")
            else:
                print(f"Unexpected record format: {record}")
    
    def show_add_record_window(self):
        # Clear existing widgets
        for widget in self.__root.winfo_children():
            widget.destroy()

        # Create new widgets for adding a record
        artist_label = tk.Label(self.__root, font=("Arial", 14), text="Artist:")
        artist_label.pack()
        self.__artist_entry = tk.Entry(self.__root, font=("Arial", 14))
        self.__artist_entry.pack()

        record_label = tk.Label(self.__root, font=("Arial", 14), text="Record:")
        record_label.pack()
        self.__record_entry = tk.Entry(self.__root, font=("Arial", 14))
        self.__record_entry.pack()

        add_button = tk.Button(self.__root, text="Add Record", font=("Arial", 14), command=self.perform_add)
        add_button.pack()

        back_button = tk.Button(self.__root, text="Back to Main", font=("Arial", 14), command=self.__setup_main_window)
        back_button.pack()

    def __setup_main_window(self):
        for widget in self.__root.winfo_children():
            widget.destroy()
        self.create_search_frame()
        self.create_results_listbox()
        self.create_reset_button()
        back_button = tk.Button(self.__root, text="To Add GUI", font=("Arial", 14), command=self.show_add_record_window)
        back_button.pack()

        #back_button2 = tk.Button(self.__root, text="To Del GUI", font=("Arial", 14), command=self.show_del_record_window)
        #back_button2.pack()

        back_button3 = tk.Button(self.__root, text="Del", font=("Arial", 14), command=self.delete_selected)
        back_button3.pack()

        self.__canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        self.reset_list()

    def show_del_record_window(self):
        # Clear existing widgets
        for widget in self.__root.winfo_children():
            widget.destroy()

        # Create new widgets for adding a record
        artist_label = tk.Label(self.__root, font=("Arial", 14), text="Artist:")
        artist_label.pack()
        self.__artist_entry = tk.Entry(self.__root, font=("Arial", 14))
        self.__artist_entry.pack()

        record_label = tk.Label(self.__root, font=("Arial", 14), text="Record:")
        record_label.pack()
        self.__record_entry = tk.Entry(self.__root, font=("Arial", 14))
        self.__record_entry.pack()

        add_button = tk.Button(self.__root, text="Del Record", font=("Arial", 14), command=self.perform_del)
        add_button.pack()

        back_button = tk.Button(self.__root, text="Back to Main", font=("Arial", 14), command=self.__setup_main_window)
        back_button.pack()

    def delete_selected(self):
        selected = self.results_listbox.curselection()  # Get selected index
        if selected:  # Check if something is selected
            item = self.results_listbox.get(selected)  # Get the text of selected item
        # Now you'll need to parse this item to get artist and record
        # How you split this depends on how you're displaying items in the listbox
        # For example if displayed as "Artist - Record":
            artist, record = item.split(" - ")  # Just an example format
            if records.del_from_records(records.records, artist, record):
                self.results_listbox.delete(selected)  # Remove from listbox
                print("-------------------")
                print("Successfully deleted:")
                print(f"Artist: {artist}")
                print(f"Record: {record}")
                print("from the database")
                print("-------------------")
        else:
            print("Nothing selected to delete")