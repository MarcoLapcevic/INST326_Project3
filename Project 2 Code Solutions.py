# imports
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime # one module for working with dates and times
import json #this solution saves and opens json files. You may use a different file type and change the import accordingly

# The MainWindow class creates a custom GUI window based on the tkinter window (tk.Tk)
# It has an __init__() method, and three additional methods (new_note(), open_notebook(), and save_notebook())
# These methods correspond to new, open, and save buttons in the window.
# The new_note method calls the NoteForm class to create a new note form top level window.

class MainWindow(tk.Tk):        # sub-class from the tkinter module.
    def __init__(self):         # initialize the main window.
        super().__init__()      # initialize it as a tkinter window.
        
        self.geometry("600x400") # set the default window size
        self.title('Notebook') # set the default window title
        self.notebook = [] # initialize an attribute named 'notebook' as an empty list
        self.notes = [] # list of note objects in the note class.
        self.note = {}

        # create a frame called frame_main that covers the entire window.
        # not required for full credit
        # all other objects will be placed in frame_main instead of the window itself
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')
        
        # create a frame in the new window that covers the entire window
        self.frame_notes = tk.Frame(self.frame_main)
        self.frame_notes.grid(row=1, column=3, rowspan=6, sticky='w')
        self.frame_notes.config(bg='gray') 
        
        # define some buttons and put them in a grid in frame_main
        # create new note button - opens a new note form
        btn01=tk.Button(self.frame_main, text='Create New Note', command=self.new_note)
        btn01.grid(padx=10, pady=10, row=1, column=1)
        
        # open notebook button - opens a notebook and displays its notes in the window
        btn02=tk.Button(self.frame_main, text='Open Notebook', command=self.open_notebook)
        btn02.grid(padx=10, pady=10, row=2, column=1) 
        
        # save notebook button - saves the notebook and refreshes the notes display
        btn03=tk.Button(self.frame_main, text='Save Notebook\nand Refresh', command=self.save_notebook)
        btn03.grid(padx=10, pady=10, row=3, column=1) 
        
        # quit button
        btn04=tk.Button(self.frame_main, text='Quit', command=self.destroy)
        btn04.grid(padx=10, pady=10, row=4, column=1)

    # define methods corresponding to the button commands
    
    # new_note opens a new toplevel window with a note form.
    # when the new note's submit button is pressed, the new note is added to the self.notebook
    # attribute in the main_window object.
     
       
    def new_note(self): # opens a new note form
        note_form = NoteForm(self, self.notebook, self.notes)
        return None

    def clear_frame(self, target_frame): # method for clearing old content from the frame
        for widgets in target_frame.winfo_children():
            widgets.destroy()

    def show_notes(self): # generates note objects and displays them in the main window
        self.clear_frame(self.frame_notes) # clears any previous display
        self.notes = [] # resets the notes object list
        for note in self.notebook: # create new note objects from the notebook and display them
            new_note = MakeNote(master=self.frame_notes, note_dict=note)
            self.notes.append(new_note)
            new_note.pack(padx=10, pady=10)
            new_note.config(height= 3, width=40, wraplength=200, justify=tk.LEFT)
        return None
    
    def open_notebook(self):
        # this opens json files. You may use different file types.
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\sdemp\\Documents\\GitHub\\Courses\\INST326\\test_files",
                                         filetypes=[("json files", "*.json"), 
                                                    ("csv files", ".csv"),
                                                    ("all files", "*.*")])
        file = open(filepath, "r")
        self.notebook = json.load(file) # load the json file into self.notebook as a list of dictionaries
        file.close()
       
        self.show_notes() # once the file is loaded, call the method to display the notes in the window
        return None
    
    def save_notebook(self):
        # the following code saves the notebook as a json file. You  may use different file types
        file = filedialog.asksaveasfile(initialdir="C:\\Users\\sdemp\\Documents\\GitHub\\Courses\\INST326\\test_files",
                                              defaultextension=".json", 
                                        title="notebook01",
                                              filetypes=[("json file", ".json"),
                                             ("all files", ".*")])
        
        json_out = json.dumps(self.notebook, indent=2)      # file gets ready to save the file as a JSON file 
        file.write(json_out)
        
        self.show_notes() # this refreshes the notes display in the main window
        return None


# the NoteForm() class creates a Toplevel window that is a note form containing fields for
# data entry for title, text, link, and tags. It also calculates a meta field with date, time, and timezone
# the Noteform class has an __init__() method, and a submit() method that is called by a submit button
# the class may contain additional methods to perform tasks like calculating the metadata, for example

class NoteForm(tk.Toplevel):
    def __init__(self, master, notebook, notes, note_to_edit=None):
        super().__init__(master)
        self.geometry("400x300")
        self.title('Note Form')
        self.notebook = notebook
        self.notes = notes
        self.note_to_edit = note_to_edit
        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.pack(pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(pady=5)
        self.text_label = ttk.Label(self, text="Text:")
        self.text_label.pack(pady=5)
        self.text_entry = tk.Text(self, width=30, height=10)
        self.text_entry.pack(pady=5)
        self.link_label = ttk.Label(self, text="Link:")
        self.link_label.pack(pady=5)
        self.link_entry = ttk.Entry(self)
        self.link_entry.pack(pady=5)
        self.tag_label = ttk.Label(self, text="Tags:")
        self.tag_label.pack(pady=5)
        self.tag_entry = ttk.Entry(self)
        self.tag_entry.pack(pady=5)
        
        # If editing existing note, populate fields with existing data
        if note_to_edit:
            self.title_entry.insert(tk.END, note_to_edit["title"])
            self.text_entry.insert(tk.END, note_to_edit["text"])
            self.link_entry.insert(tk.END, note_to_edit["link"])
            self.tag_entry.insert(tk.END, note_to_edit["tags"])

        submit_button = ttk.Button(self, text="Submit", command=self.submit)
        submit_button.pack(pady=5)

    def submit(self):
        title = self.title_entry.get()
        text = self.text_entry.get("1.0", tk.END)
        link = self.link_entry.get()
        tags = self.tag_entry.get()  
        metadata = {
            "timestamp": datetime.datetime.now().isoformat(),
            "timezone": datetime.datetime.now().astimezone().tzinfo.name}
        
        note_dict = {
            "title": title,
            "text": text,
            "link": link,
            "tags": tags,
            "metadata": metadata}
        
        if self.note_to_edit:  # If editing existing note, update instead of appending
            self.notes.remove(self.note_to_edit)
        self.notes.append(note_dict)
        self.master.display_notes()
        self.destroy()
    
    def save_snippet_to_file(text, filename):
        with open(filename, "w") as file:
            file.write(text)

    def read_snippet_from_file(filename):
        with open(filename, "r") as file:
            return file.read()

    def display_snippet(text, language):
        print("Snippet Language:", language)
        print("Snippet Text:", text)

    def edit_snippet(text, new_text):
        return new_text

class MakeNote(tk.Button):
    def __init__(self, master=None, note_dict=None): # the arguments on this line
        # are inbound, meaning we pass them when we instantiate the object
        super().__init__(master) # on this line we call the __init__ method of tk.Button and pass
        # the master attribute to it. This gives us all the button attributes and functionality
        
        # define note attributes
        self.title = note_dict['title']
        self.text = note_dict['text']
        self.link = note_dict['link']
        self.tags = note_dict['tags']
        self.meta = note_dict['meta']

        # configure note button; this creates a button with two lines of text
        self.config(bg='light gray', text=f"{self.title}\n{self.meta}")
        
        # Bind mouse events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.note_open)

    def on_hover(self, event): # change the background when the cursor hovers over it
        self.config(bg="lightblue")  

    def on_leave(self, event): # change back when not hovering
        self.config(bg="light gray")  # Restore original color
        
    def note_open(self, event): # on mouse click, open note in new top window
        
        # create a new top window
        self.note_window = tk.Toplevel(main_window, bg="light gray", height=600, width=600)
        self.note_window.title(self.title)
        
        # create a frame in the new window that covers the entire window
        self.frame_main = tk.Frame(self.note_window)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')
        
        # create labels in the frame
        title_label = tk.Label(self.frame_main, bg='light gray', text='Note Title:')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')
        title_content = tk.Label(self.frame_main, bg='light gray', text=self.title, wraplength=400, justify=tk.LEFT)
        title_content.grid(padx=10, pady=10, row=1, column=1, sticky='w')        

        text_label = tk.Label(self.frame_main, bg='light gray', text='Note Text:')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')
        text_content = tk.Label(self.frame_main, bg='light gray', text=self.text, wraplength=400, justify=tk.LEFT)
        text_content.grid(padx=10, pady=10, row=2, column=1, sticky='w')

        link_label = tk.Label(self.frame_main, bg='light gray', text='Note Link:')
        link_label.grid(padx=10, pady=10, row=3, column=0, sticky='e')
        link_content = tk.Label(self.frame_main, bg='light gray', text=self.link, wraplength=400, justify=tk.LEFT)
        link_content.grid(padx=10, pady=10, row=3, column=1, sticky='w')
        
        tag_label = tk.Label(self.frame_main, bg='light gray', text='Note Tags:')
        tag_label.grid(padx=10, pady=10, row=4, column=0, sticky='e')
        tag_content = tk.Label(self.frame_main, bg='light gray', text=self.tags, wraplength=400, justify=tk.LEFT)
        tag_content.grid(padx=10, pady=10, row=4, column=1, sticky='w')

        meta_label = tk.Label(self.frame_main, bg='light gray', text='Note Meta:')
        meta_label.grid(padx=10, pady=10, row=5, column=0, sticky='e')
        meta_content = tk.Label(self.frame_main, bg='light gray', text=self.meta, wraplength=400, justify=tk.LEFT)
        meta_content.grid(padx=10, pady=10, row=5, column=1, sticky='w')        

        # create a button to close the note window
        b10 = tk.Button(self.frame_main, text='close', command=self.note_window.destroy)
        b10.grid(padx=10, pady=10, row=6, column=0)
        

# main execution

if __name__ == '__main__':
    
    main_window = MainWindow() # this creates a notebook / main window called main_window. You may change the name if you want

    main_window.mainloop()