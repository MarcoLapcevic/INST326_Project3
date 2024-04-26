# How to set up Frames and Labels in Object-Oriented Format using the Tkinter 
# Module.

import tkinter as tk

class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Frame & Label Window")
        self.geometry("800x600")
        
        self.frame = tk.Frame(self)
        self.frame.pack(pady = 20)
        self.frame.config(bg = "green")
        
        self.label = tk.Label(self.frame, text = "label within frame")
        self.label.pack(padx = 30, pady = 30)
        
if __name__ == "__main__":
    main_window = Main_Window()
    main_window.mainloop()