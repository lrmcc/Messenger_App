import tkinter as tk

'''
1. GUI needs to launch to Landing area 
2.1 Landing area should have an entry box to collects a username
2.2 Landing area should have an button to submit a username
3. Username submission should launch to chat window
4. Chat window should list dialogue that scrolls with addition
4.1 Chat window should have an area to submit  
4.2 Chat window should have a method to toggle direct messaging
4.3 Chat window should have a method to see users online

Build resource: https://realpython.com/python-gui-tkinter/#building-your-first-python-gui-application-with-tkinter
'''
class MessengerGUI():
    def __init__(self):
        self.message_header = ""
        self.last_message_sent = ""

    def start(self):
        window = tk.Tk()
        
        greeting = tk.Label(text="Hello, Tkinter")
        greeting.pack()
        
        label1 = tk.Label(
            text="Hello, Tkinter",
            foreground="white",  # Set the text color to white
            background="black"  # Set the background color to black
            )
        label1.pack()
        label2 = tk.Label(text="Hello, Tkinter", background="#34A2FE")
        label2.pack()
        label3 = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
        label3.pack()
        label4 = tk.Label(
            text="Hello, Tkinter",
            fg="white",
            bg="black",
            width=10,
            height=10
            )
        label4.pack()
        
        button0 = tk.Button(
            text="Click me!",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            )
        button0.pack()
        
        label0 = tk.Label(text="Name")
        label0.pack()
        
        entry0 = tk.Entry()
        entry0.pack()
        '''
        three main operations that you can perform with Entry widgets:
            Retrieving text with .get()
            Deleting text with .delete()
            Inserting text with .insert()
        '''
        entry1 = tk.Entry(fg="yellow", bg="blue", width=50)
        entry1.insert(0, "Python")
        entry1.pack()
        entry1.delete(0, tk.END) # delete to end
        
        # Do you still have the window from the previous section open?
        # If so, then you can close it by executing the following:
        # window.destroy()
        
        window = tk.Tk()
        text_box = tk.Text()
        text_box.pack()
        
        # Just like Entry widgets, 
        # you can retrieve the text from a Text widget using .get().
        # However, calling .get() with no arguments 
        # doesn’t return the full text in the text box
        # like it does for Entry widgets
        
        # Text.get() required at least one argument. 
        # Calling .get() with a single index returns a single character. 
        # To retrieve several characters, you need to pass a start index and an end index. 
        # Indices in Text widgets work differently than Entry widgets. 
        
        # Since Text widgets can have several lines of text, 
        # an index must contain two pieces of information:
        # The line number of a character
        # The position of a character on that line
        # Line numbers start with 1, and character positions start with 0. 
        # To make an index, you create a string of the form "<line>.<char>", 
        # replacing <line> with the line number and <char> with the character number. 
        
        # For example, "1.0" represents the first character on the first line, 
        # and "2.3" represents the fourth character on the second line.
        # To get all of the text in a text box, 
        # set the starting index in "1.0" 
        # and use the special tk.END constant for the second index:
        
        text_box.get("1.0", tk.END)
        
        #to clear out the rest of the text in the text box. 
        # Set "1.0" as the start index and use tk.END for the second index:
        
        text_box.delete("1.0", tk.END)
        
        #You can insert text into a text box using .insert():
        
        text_box.insert("1.0", "Hello")
        # insert() will do one of two things:
        # Insert text at the specified position if there’s already text at or after that position.
        # Append text to the specified line if the character number is greater than the index of the last character in the text box.
        # It’s usually impractical to try and keep track of what the index of the last character is. The best way to insert text at the end of a Text widget is to pass tk.END to the first parameter of .insert():

        text_box.insert(tk.END, "\nPut me at the end!")
        
        #Frame widgets are important for organizing the layout of your widgets in an application.
        
        frame = tk.Frame()
        frame.pack()
        
        # frame.pack() packs the frame into the window 
        # so that the window sizes itself as small as possible to encompass the frame.
        # An empty Frame widget is practically invisible. 
        # Frames are best thought of as containers for other widgets. 
        # You can assign a widget to a frame by setting the widget’s master attribute:
        
        frame = tk.Frame()
        
        label = tk.Label(master=frame)
        
        # The following creates two Frame widgets called frame_a and frame_b. 
        # In this script, frame_a contains a label with the text "I'm in Frame A", 
        # and frame_b contains the label "I'm in Frame B". Here’s one way to do this:
        
        frame_a = tk.Frame()
        frame_b = tk.Frame()

        label_a = tk.Label(master=frame_a, text="I'm in Frame A")
        label_a.pack()

        label_b = tk.Label(master=frame_b, text="I'm in Frame B")
        label_b.pack()

        frame_a.pack()
        frame_b.pack()
        
        '''
        All four of the widget types you’ve learned about
        —Label, Button, Entry, and Text—
        have a master attribute that’s set when you instantiate them. 
        That way, you can control which Frame a widget is assigned to. 
        Frame widgets are great for organizing other widgets in a logical manner. 
        Related widgets can be assigned to the same frame so that, 
        if the frame is ever moved in the window, 
        then the related widgets stay together.'''
        
        border_effects = {
            "flat": tk.FLAT,
            "sunken": tk.SUNKEN,
            "raised": tk.RAISED,
            "groove": tk.GROOVE,
            "ridge": tk.RIDGE,
            }

        for relief_name, relief in border_effects.items():
            frame = tk.Frame(master=window, relief=relief, borderwidth=5)
            frame.pack(side=tk.LEFT)
            label = tk.Label(master=frame, text=relief_name)
            label.pack()
        
        # Application layout in Tkinter is controlled with geometry managers. 
        # While .pack() is an example of a geometry manager, it isn’t the only one. 
        # Tkinter has two others:
        # .place()
        # .grid()
        
        '''
        The side keyword argument of .pack() specifies 
        on which side of the window the widget should be placed. 
        These are the available options:
            tk.TOP
            tk.BOTTOM
            tk.LEFT
            tk.RIGHT
        '''
        
        frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
        frame1.pack(fill=tk.Y, side=tk.LEFT)

        frame2 = tk.Frame(master=window, width=100, bg="yellow")
        frame2.pack(fill=tk.Y, side=tk.LEFT)

        frame3 = tk.Frame(master=window, width=50, bg="blue")
        frame3.pack(fill=tk.Y, side=tk.LEFT)
        
        
        
        window.mainloop()
        