from tkinter import Tk, BOTH, Canvas, NW
import records
import tkinter as tk
import os
import shared
import sys
import time
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title('VinylDB')
        self.__root.geometry(f"{width}x{height}")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__root.configure(bg='#2c3e50')
        
        self.setup_styles()
        
        self.width = width
        self.height = height
        self.current_records = []
        self.__setup_main_window()

    def setup_styles(self):
        style = ttk.Style()
        
        style.configure('Modern.TEntry',
                       fieldbackground='#ecf0f1',
                       borderwidth=0,
                       insertcolor='#34495e',
                       relief='flat')
        
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=0)

    def create_header_frame(self):
        header_frame = tk.Frame(self.__root, bg='#34495e', height=5)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

    def create_search_frame(self):
        search_container = tk.Frame(self.__root, bg='#2c3e50', height=80)
        search_container.pack(fill=tk.X, padx=30, pady=20)
        search_container.pack_propagate(False)
        
        search_input_frame = tk.Frame(search_container, bg='#2c3e50')
        search_input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_entry = tk.Entry(search_input_frame,
                                   font=("Helvetica", 14),
                                   bg='#ecf0f1',
                                   fg='#2c3e50',
                                   relief='flat',
                                   borderwidth=0,
                                   insertbackground='#34495e')
        self.search_entry.pack(fill=tk.X, ipady=12, ipadx=15)
        
        shadow_frame = tk.Frame(search_input_frame, bg='#bdc3c7', height=2)
        shadow_frame.pack(fill=tk.X)
        
        self.search_entry.bind('<Return>', lambda event: self.perform_search()) # search on enter
        self.search_entry.bind('<KeyRelease>', self.on_search_change) # update search results on typing
        
        button_frame = tk.Frame(search_container, bg='#2c3e50')
        button_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        button_config = {
            'font': ("Helvetica", 12, 'bold'),
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 25,
            'pady': 12,
            'cursor': 'arrow'
        }
        
        search_btn = tk.Button(button_frame,
                              text="Search",
                              bg='#27ae60',
                              fg='white',
                              activebackground='#2ecc71',
                              activeforeground='white',
                              command=self.perform_search,
                              **button_config)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(button_frame,
                           text="Add",
                           bg='#3498db',
                           fg='white',
                           activebackground='#5dade2',
                           activeforeground='white',
                           command=self.show_add_record_window,
                           **button_config)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        shuffle_btn = tk.Button(button_frame,
                               text="Shuffle",
                               bg='#f39c12',
                               fg='white',
                               activebackground='#f4d03f',
                               activeforeground='white',
                               command=self.shuffle_record,
                               **button_config)
        shuffle_btn.pack(side=tk.LEFT, padx=5)

    def create_main_content_frame(self):
        content_frame = tk.Frame(self.__root, bg='#2c3e50')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        left_panel_frame = tk.Frame(content_frame, bg='#2c3e50')
        left_panel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.left_panel = tk.Frame(left_panel_frame, bg='white', relief='flat')
        self.left_panel.pack(fill=tk.BOTH, expand=True)
        
        shadow_left = tk.Frame(left_panel_frame, bg='#95a5a6', height=3)
        shadow_left.pack(fill=tk.X, side=tk.BOTTOM)
        
        list_header_frame = tk.Frame(self.left_panel, bg='#34495e', height=50)
        list_header_frame.pack(fill=tk.X)
        list_header_frame.pack_propagate(False)
        
        list_header = tk.Label(list_header_frame,
                             text="Record Collection",
                             font=("Helvetica", 16, 'bold'),
                             bg='#34495e',
                             fg='white')
        list_header.pack(pady=12)
        
        listbox_container = tk.Frame(self.left_panel, bg='white')
        listbox_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.results_listbox = tk.Listbox(listbox_container,
                                        font=("Helvetica", 14),
                                        bg='white',
                                        fg='#2c3e50',
                                        selectbackground='#3498db',
                                        selectforeground='white',
                                        relief='flat',
                                        borderwidth=0,
                                        highlightthickness=0,
                                        activestyle='none')
        
        scrollbar = tk.Scrollbar(listbox_container, orient=tk.VERTICAL,
                           bg='#95a5a6',           # Light gray thumb
                           troughcolor='#ecf0f1',  # Light track  
                           activebackground='#3498db', # Blue when active
                           highlightthickness=0,    # No border highlight
                           borderwidth=0,           # No border
                           width=10)                # Medium width
        
        self.results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_listbox.yview)
        
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox.bind('<<ListboxSelect>>', self.on_record_select)
        
        right_panel_frame = tk.Frame(content_frame, bg='#2c3e50', width=350)
        right_panel_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        right_panel_frame.pack_propagate(False)
        
        self.right_panel = tk.Frame(right_panel_frame, bg='white', relief='flat')
        self.right_panel.pack(fill=tk.BOTH, expand=True)
        
        shadow_right = tk.Frame(right_panel_frame, bg='#95a5a6', height=3)
        shadow_right.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.show_welcome_message()
        self.create_status_bar()

    def create_status_bar(self):
        status_frame = tk.Frame(self.__root, bg='#34495e', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                   text=f"Ready - {len(records.records)} records in collection",
                                   font=("Helvetica", 10),
                                   bg='#34495e',
                                   fg='#ecf0f1')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)

    def update_status(self, message):
        self.status_label.config(text=message)

    def on_search_change(self, event):
        if hasattr(self, '_search_timer'):
            self.__root.after_cancel(self._search_timer)
        
        # wait 300ms after user stops typing
        self._search_timer = self.__root.after(300, self.perform_search)

    def show_welcome_message(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        header_frame = tk.Frame(self.right_panel, bg='#34495e', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame,
                              text="Record Details",
                              font=("Helvetica", 16, 'bold'),
                              bg='#34495e',
                              fg='white')
        header_label.pack(pady=12)
        
        content_frame = tk.Frame(self.right_panel, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        welcome_title = tk.Label(content_frame,
                               text="Welcome to VinylDB",
                               font=("Helvetica", 18, 'bold'),
                               bg='white',
                               fg='#2c3e50')
        welcome_title.pack(pady=(0, 20))
        
        instructions = [
            "Select a record to view details",
            "Use search to find records", 
            "Try shuffle for random picks",
            "Add new records to grow your collection"
        ]
        
        for instruction in instructions:
            inst_label = tk.Label(content_frame,
                                text=instruction,
                                font=("Helvetica", 11),
                                bg='white',
                                fg='#7f8c8d',
                                justify=tk.LEFT)
            inst_label.pack(anchor=tk.W, pady=2)

    def show_record_details(self, artist, record, edit_mode=False):
        self.__root.unbind_all("<MouseWheel>")
        self.__root.unbind_all("<Button-4>")
        self.__root.unbind_all("<Button-5>")
        
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        header_frame = tk.Frame(self.right_panel, bg='#34495e', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_text = "Edit Record" if edit_mode else "Record Details"
        header_label = tk.Label(header_frame,
                            text=header_text,
                            font=("Helvetica", 16, 'bold'),
                            bg='#34495e',
                            fg='white')
        header_label.pack(pady=12)
        
        record_data = self.get_record_data(artist, record)
        
        button_frame = tk.Frame(self.right_panel, bg='white', height=120)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        button_frame.pack_propagate(False)
        
        if edit_mode:
            confirm_btn = tk.Button(button_frame,
                                text="Confirm Changes",
                                font=("Helvetica", 12, 'bold'),
                                bg='#27ae60',
                                fg='white',
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=12,
                                cursor='arrow',
                                command=self.confirm_edit)
            confirm_btn.pack(fill=tk.X, pady=(0, 10))
            
            cancel_btn = tk.Button(button_frame,
                                text="Cancel",
                                font=("Helvetica", 12, 'bold'),
                                bg='#95a5a6',
                                fg='white',
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=12,
                                cursor='arrow',
                                command=self.cancel_edit)
            cancel_btn.pack(fill=tk.X)
        else:
            edit_btn = tk.Button(button_frame,
                                text="Edit Record",
                                font=("Helvetica", 12, 'bold'),
                                bg='#3498db',
                                fg='white',
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=12,
                                cursor='arrow',
                                command=lambda: self.show_record_details(record_data["Artist"], record_data["Record"], edit_mode=True))
            edit_btn.pack(fill=tk.X, pady=(0, 10))
            
            delete_btn = tk.Button(button_frame,
                                text="Delete Record",
                                font=("Helvetica", 12, 'bold'),
                                bg='#e74c3c',
                                fg='white',
                                relief='flat',
                                borderwidth=0,
                                padx=20,
                                pady=12,
                                cursor='arrow',
                                command=lambda: self.delete_specific_record(record_data["Artist"], record_data["Record"]))
            delete_btn.pack(fill=tk.X)
        
        # Scrollable Area Logic
        canvas_frame = tk.Frame(self.right_panel, bg='white')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))
        
        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", 
                           command=canvas.yview,    # Command to affect the canvas
                           bg='#95a5a6',           # Light gray thumb
                           troughcolor='#ecf0f1',  # Light track
                           activebackground='#3498db', # Blue when active  
                           highlightthickness=0,    # No border highlight
                           borderwidth=0,           # No border
                           width=10)                # Medium width
        
        self.current_canvas = canvas
        scrollable_frame = tk.Frame(canvas, bg='white')
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event=None):
            if canvas.winfo_exists():  # Check if canvas still exists
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas_width = canvas.winfo_width()
                canvas.itemconfig(canvas_window, width=canvas_width)

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        def _on_mousewheel(event):
            """Cross-platform mouse wheel scrolling"""
            if hasattr(self, 'current_canvas') and self.current_canvas.winfo_exists():
                # Windows and macOS
                if hasattr(event, 'delta') and event.delta:
                    self.current_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                # Linux
                elif hasattr(event, 'num'):
                    if event.num == 4:
                        self.current_canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        self.current_canvas.yview_scroll(1, "units")
        
        # Store the event function
        self._on_mousewheel = _on_mousewheel
        
        def on_enter(event):
            # Bind for Windows/macOS
            self.__root.bind_all("<MouseWheel>", self._on_mousewheel)
            # Bind for Linux  
            self.__root.bind_all("<Button-4>", self._on_mousewheel)
            self.__root.bind_all("<Button-5>", self._on_mousewheel)
        
        def on_leave(event):
            # Unbind all mouse wheel events
            self.__root.unbind_all("<MouseWheel>")
            self.__root.unbind_all("<Button-4>")
            self.__root.unbind_all("<Button-5>")
        
        # Bind to multiple widgets to ensure it works
        self.right_panel.bind("<Enter>", on_enter)
        self.right_panel.bind("<Leave>", on_leave)
        canvas_frame.bind("<Enter>", on_enter)
        canvas_frame.bind("<Leave>", on_leave)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        
        if edit_mode:
            self.show_edit_fields(scrollable_frame, record_data)
        else:
            self.show_view_fields(scrollable_frame, record_data)
        
        self.right_panel.after(1, configure_scroll_region)

    def get_record_data(self, artist, record):
        for rec in records.records:
            if isinstance(rec, dict):
                if rec.get("Artist") == artist and rec.get("Record") == record:
                    return {
                        "Artist": rec.get("Artist", artist),
                        "Record": rec.get("Record", record),
                        "Year": rec.get("Year", ""),
                        "Rating": rec.get("Rating", ""),
                        "Notes": rec.get("Notes", ""),
                        "Price": rec.get("Price", "")
                    }
            elif isinstance(rec, list) and len(rec) >= 2:
                if rec[0] == artist and rec[1] == record:
                    return {
                        "Artist": rec[0],
                        "Record": rec[1],
                        "Year": rec[2] if len(rec) > 2 else "",
                        "Rating": rec[3] if len(rec) > 3 else "",
                        "Notes": rec[4] if len(rec) > 4 else "",
                        "Price": rec[5] if len(rec) > 5 else ""
                    }
        
        return {
            "Artist": artist,
            "Record": record,
            "Year": "",
            "Rating": "",
            "Notes": "",
            "Price": ""
        }

    def show_view_fields(self, parent, record_data):
        self.current_record_data = record_data
        

        self.create_view_field(parent, "Artist", record_data["Artist"])
        self.create_view_field(parent, "Album", record_data["Record"])
        self.create_view_field(parent, "Year", record_data["Year"] or "Not specified")
        rating_text = f"{record_data['Rating']}/5 stars" if record_data["Rating"] else "Not rated"
        self.create_view_field(parent, "Rating", rating_text)
        price_text = f"${record_data['Price']}" if record_data["Price"] else "Not specified"
        self.create_view_field(parent, "Price", price_text)
        notes_text = record_data["Notes"] if record_data["Notes"] else "No notes"
        self.create_view_field(parent, "Notes", notes_text, multiline=True)

    def show_edit_fields(self, parent, record_data):
        self.original_record_data = record_data.copy()
        self.edit_widgets = {}

        self.edit_widgets["Artist"] = self.create_edit_field(parent, "Artist", record_data["Artist"])
        self.edit_widgets["Record"] = self.create_edit_field(parent, "Album", record_data["Record"])
        self.edit_widgets["Year"] = self.create_edit_field(parent, "Year", record_data["Year"])
        self.edit_widgets["Rating"] = self.create_edit_field(parent, "Rating (1-5)", record_data["Rating"])
        self.edit_widgets["Price"] = self.create_edit_field(parent, "Price ($)", record_data["Price"])
        self.edit_widgets["Notes"] = self.create_edit_field(parent, "Notes", record_data["Notes"], multiline=True)

    def create_view_field(self, parent, label, value, multiline=False):
        field_frame = tk.Frame(parent, bg='#f8f9fa', relief='flat')
        field_frame.pack(fill=tk.X, pady=(0, 10), padx=10, ipady=10)
        
        tk.Label(field_frame,
                text=label,
                font=("Helvetica", 11, 'bold'),
                bg='#f8f9fa',
                fg='#7f8c8d').pack(anchor=tk.W, padx=15, pady=(5, 0))
        
        if multiline and len(str(value)) > 50:
            text_widget = tk.Text(field_frame,
                                 font=("Helvetica", 12),
                                 bg='#f8f9fa',
                                 fg='#2c3e50',
                                 relief='flat',
                                 borderwidth=0,
                                 wrap=tk.WORD,
                                 height=3,
                                 state='disabled')
            text_widget.pack(fill=tk.X, padx=15, pady=(0, 5))
            text_widget.config(state='normal')
            text_widget.insert('1.0', str(value))
            text_widget.config(state='disabled')
        else:
            tk.Label(field_frame,
                    text=str(value),
                    font=("Helvetica", 12, 'bold'),
                    bg='#f8f9fa',
                    fg='#2c3e50',
                    wraplength=280,
                    justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(0, 5))

    def create_edit_field(self, parent, label, value, multiline=False):
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(field_frame,
                text=label,
                font=("Helvetica", 11, 'bold'),
                bg='white',
                fg='#2c3e50').pack(anchor=tk.W, pady=(0, 5))
        
        if multiline:
            widget = tk.Text(field_frame,
                           font=("Helvetica", 12),
                           bg='#ecf0f1',
                           fg='#2c3e50',
                           relief='flat',
                           borderwidth=0,
                           wrap=tk.WORD,
                           height=4,
                           insertbackground='#34495e')
            widget.pack(fill=tk.X, ipady=8, ipadx=12)
            widget.insert('1.0', str(value))
        else:
            widget = tk.Entry(field_frame,
                            font=("Helvetica", 12),
                            bg='#ecf0f1',
                            fg='#2c3e50',
                            relief='flat',
                            borderwidth=0,
                            insertbackground='#34495e')
            widget.pack(fill=tk.X, ipady=8, ipadx=12)
            widget.insert(0, str(value))
        
        return widget

    def confirm_edit(self):
        new_data = {}
        for field, widget in self.edit_widgets.items():
            if isinstance(widget, tk.Text):
                value = widget.get('1.0', 'end-1c').strip()
            else:
                value = widget.get().strip()
            new_data[field] = value
        
        if new_data["Rating"] and new_data["Rating"] not in ["1", "2", "3", "4", "5"]:
            self.update_status("Rating must be 1-5 or empty")
            return
        
        old_artist = self.original_record_data["Artist"]
        old_record = self.original_record_data["Record"]
        records.del_from_records(records.records, old_artist, old_record)
        
        records.records.append({
            "Artist": new_data["Artist"],
            "Record": new_data["Record"],
            "Year": new_data["Year"],
            "Rating": new_data["Rating"],
            "Notes": new_data["Notes"],
            "Price": new_data["Price"]
        })
        
        records.save_records(records.records)
        records.records = records.load_records()
        
        self.reset_list()
        self.show_record_details(new_data["Artist"], new_data["Record"])
        self.update_status(f"Updated: {new_data['Artist']} - {new_data['Record']}")

    def cancel_edit(self):
        orig = self.original_record_data
        self.show_record_details(orig["Artist"], orig["Record"])
        self.update_status("Edit cancelled")

    def on_record_select(self, event):
        selection = self.results_listbox.curselection()
        if selection:
            item = self.results_listbox.get(selection[0])
            if item != "No Results Found" and " | " in item:
                artist, record = item.split(" | ", 1)
                self.show_record_details(artist, record)
                self.update_status(f"Viewing: {artist} - {record}")

    def perform_search(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.reset_list()
            return
        
        results = records.search_records(records.records, search_term)
        self.display_results(results)
        self.update_status(f"Found {len(results)} records matching '{search_term}'")

    def display_results(self, results):
        self.results_listbox.delete(0, tk.END)
        self.current_records = results
        
        if results:
            for result in results:
                artist = result["Artist"]
                record = result["Record"]
                display_string = f"{artist} | {record}"
                self.results_listbox.insert(tk.END, display_string)
        else:
            self.results_listbox.insert(tk.END, "No Results Found")
            
        if not results:
            self.show_welcome_message()

    def shuffle_record(self):
        if not records.records:
            self.update_status("Collection is empty - add some records first!")
            return
        
        self.update_status("Shuffling...")
        self.__root.update()
        
        self.__root.after(500, self._complete_shuffle)

    def _complete_shuffle(self):
        random_record = random.choice(records.records)
        
        self.search_entry.delete(0, tk.END)
        self.reset_list()
        
        if isinstance(random_record, list):
            artist, record = random_record[0], random_record[1]
        else:
            artist, record = random_record["Artist"], random_record["Record"]
        
        display_string = f"{artist} | {record}"
        
        for i in range(self.results_listbox.size()):
            if self.results_listbox.get(i) == display_string:
                self.results_listbox.selection_clear(0, tk.END)
                self.results_listbox.selection_set(i)
                self.results_listbox.see(i)
                self.show_record_details(artist, record)
                break
        
        self.update_status(f"Random pick: {artist} - {record}")

    def reset_list(self):
        self.results_listbox.delete(0, tk.END)
        self.current_records = records.records.copy()
        
        for record in records.records:
            if isinstance(record, list):
                self.results_listbox.insert(tk.END, f"{record[0]} | {record[1]}")
            elif isinstance(record, dict):
                self.results_listbox.insert(tk.END, f"{record['Artist']} | {record['Record']}")
        
        self.search_entry.delete(0, tk.END)
        self.show_welcome_message()
        self.update_status(f"Showing all {len(records.records)} records")

    def delete_specific_record(self, artist, record):
        if records.del_from_records(records.records, artist, record):
            print(f"Successfully deleted: {artist} - {record}")
            self.reset_list()
            self.show_welcome_message()
            self.update_status(f"Deleted: {artist} - {record}")
        else:
            self.update_status("Failed to delete record")

    def show_add_record_window(self):
        for widget in self.__root.winfo_children():
            widget.destroy()
        
        self.create_header_frame()
        
        main_frame = tk.Frame(self.__root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        card_frame = tk.Frame(main_frame, bg='white', relief='flat')
        card_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        card_header = tk.Frame(card_frame, bg='#34495e', height=60)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        
        tk.Label(card_header,
                text="Add New Record",
                font=("Helvetica", 18, 'bold'),
                bg='#34495e',
                fg='white').pack(pady=15)
        
        button_frame = tk.Frame(card_frame, bg='white', height=100)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=40, pady=20)
        button_frame.pack_propagate(False)
        
        button_style = {
            'font': ("Helvetica", 14, 'bold'),
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 30,
            'pady': 15,
            'cursor': 'arrow'
        }
        
        add_btn = tk.Button(button_frame,
                        text="Add Record",
                        bg='#27ae60',
                        fg='white',
                        activebackground='#2ecc71',
                        command=self.perform_add_full,
                        **button_style)
        add_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        back_btn = tk.Button(button_frame,
                            text="Back to Collection",
                            bg='#95a5a6',
                            fg='white',
                            activebackground='#7f8c8d',
                            command=self.__setup_main_window,
                            **button_style)
        back_btn.pack(side=tk.LEFT)
        
        # Scrollable Area Logic
        canvas_frame = tk.Frame(card_frame, bg='white')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(30, 0))
        
        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg='white')
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        def _on_mousewheel(event):
            """Cross-platform mouse wheel scrolling for add record window"""
            # Windows and macOS
            if hasattr(event, 'delta') and event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # Linux
            elif hasattr(event, 'num'):
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        def on_enter(event):
            # Bind for Windows/macOS
            self.__root.bind_all("<MouseWheel>", _on_mousewheel)
            # Bind for Linux  
            self.__root.bind_all("<Button-4>", _on_mousewheel)
            self.__root.bind_all("<Button-5>", _on_mousewheel)
        
        def on_leave(event):
            # Unbind all mouse wheel events
            self.__root.unbind_all("<MouseWheel>")
            self.__root.unbind_all("<Button-4>")
            self.__root.unbind_all("<Button-5>")
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
        self.add_widgets = {}
        self.add_widgets["Artist"] = self.create_add_field(scrollable_frame, "Artist (required)", "")
        self.add_widgets["Record"] = self.create_add_field(scrollable_frame, "Album (required)", "")
        self.add_widgets["Year"] = self.create_add_field(scrollable_frame, "Year", "")
        self.add_widgets["Rating"] = self.create_add_field(scrollable_frame, "Rating (1-5)", "")
        self.add_widgets["Price"] = self.create_add_field(scrollable_frame, "Price ($)", "")
        self.add_widgets["Notes"] = self.create_add_field(scrollable_frame, "Notes", "", multiline=True)
        
        card_frame.after(1, configure_scroll_region)
        
        self.add_widgets["Artist"].focus()

    def create_add_field(self, parent, label, value, multiline=False):
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(field_frame,
                text=label,
                font=("Helvetica", 11, 'bold'),
                bg='white',
                fg='#2c3e50').pack(anchor=tk.W, pady=(0, 5))
        
        if multiline:
            widget = tk.Text(field_frame,
                           font=("Helvetica", 12),
                           bg='#ecf0f1',
                           fg='#2c3e50',
                           relief='flat',
                           borderwidth=0,
                           wrap=tk.WORD,
                           height=4,
                           insertbackground='#34495e')
            widget.pack(fill=tk.X, ipady=8, ipadx=12)
            if value:
                widget.insert('1.0', str(value))
        else:
            widget = tk.Entry(field_frame,
                            font=("Helvetica", 12),
                            bg='#ecf0f1',
                            fg='#2c3e50',
                            relief='flat',
                            borderwidth=0,
                            insertbackground='#34495e')
            widget.pack(fill=tk.X, ipady=8, ipadx=12)
            if value:
                widget.insert(0, str(value))
        
        return widget

    def perform_add_full(self):
        new_data = {}
        for field, widget in self.add_widgets.items():
            if isinstance(widget, tk.Text):
                value = widget.get('1.0', 'end-1c').strip()
            else:
                value = widget.get().strip()
            new_data[field] = value
        
        if not new_data["Artist"] or not new_data["Record"]:
            self.update_status("Artist and Album are required")
            return
        
        if new_data["Rating"] and new_data["Rating"] not in ["1", "2", "3", "4", "5"]:
            self.update_status("Rating must be 1-5 or empty")
            return
        
        records.records.append(new_data)
        records.save_records(records.records)
        records.records = records.load_records()
        
        print(f"Successfully added: {new_data['Artist']} - {new_data['Record']}")
        self.__setup_main_window()
        self.update_status(f"Added: {new_data['Artist']} - {new_data['Record']}")

    def close(self):
        self.__running = False
        self.__root.destroy()
        print("VinylDB closed")

    def run(self):
        self.__root.mainloop()

    def get_title(self):
        return self.__root.title()

    def get_root(self):
        return self.__root

    def __setup_main_window(self):
        for widget in self.__root.winfo_children():
            widget.destroy()
        
        self.create_header_frame()
        self.create_search_frame()
        self.create_main_content_frame()
        self.reset_list()