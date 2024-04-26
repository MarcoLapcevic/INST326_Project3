import tkinter as tk

class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Main Window")
        self.geometry("800x600")
        self.config(bg = "green")
        
        self.frame = tk.Frame(self, bg = "light gray")
        self.frame.pack(pady = 30)
        
        button_1 = tk.Button(self.frame, text = "Click to Open a New Window", command = self.new_window)
        button_1.pack()
        
    def new_window(self):
        new_window = New_Window(self)
        

class New_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("New Window")
        self.geometry("700x500")
        self.config(bg = "light gray")
        
if __name__ == "__main__":
    main_window = Main_Window()
    main_window.mainloop()