#!/usr/bin/env python3

import tkinter as tk

from messenger_package.Messenger_Functions import *
from messenger_package.Messenger_Client import *

'''
1. GUI needs to launch to login area
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
        self.USERNAME = ""
        self.CLIENT = MessengerClient()
        self.chat = ""
        self.button = False
    
    def get_username(self):
        while self.USERNAME == "":
            pass
        return self.USERNAME 
    

    
    def set_geometry(self, WINDOW, width, height):
        w =  width
        h = height
        x_coord = (WINDOW.winfo_screenwidth()/2) - (w/2)
        y_coord = ((WINDOW.winfo_screenheight()/2) - (h/2)) * .5
        WINDOW.geometry('%dx%d+%d+%d' % (w, h, x_coord, y_coord))
    
     
    def start(self, ADDR, SOCK, WINDOW):
        print("Messenger_GUI.py: start(self, ADDR, SOCK, WINDOW):")
        
        w = 300
        h = 200
        
        WINDOW.title('Messenger_App')

        self.frm_main = tk.Frame(master=WINDOW, width=w, height=h)
        
        self.frm_text_display = tk.Frame(master=self.frm_main)
        self.lbl_text_display = tk.Label(master=self.frm_text_display)
        
        self.frm_text_dscrptn = tk.Frame(master=self.frm_main)
        self.lbl_text_dscrptn = tk.Label(master=self.frm_text_dscrptn,
                                  text="Enter username to join:")
        
        self.frm_text_input = tk.Frame(master=self.frm_main)
        self.ent_text_input = tk.Entry(master=self.frm_text_input)
        
        self.frm_submit = tk.Frame(master=self.frm_main)
        self.btn_submit = tk.Button(
            master=self.frm_submit,
            text="Submit",
            width=17,
            height=5
        )
        
        def handle_click(event):
            print(f"def handle_click(event), where event: {event}")
            if self.USERNAME == "":
                self.USERNAME = self.ent_text_input.get()
                print(f"self.USERNAME == {self.USERNAME}")
                self.ent_text_input.delete(0, tk.END)
                self.lbl_text_display.config(bg="gray")
                self.lbl_text_display["text"] = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                self.lbl_text_dscrptn["text"] = "To chat room:"
                self.frm_main.pack_forget()
                self.frm_main.pack(padx=50, pady=50)
                self.set_geometry(WINDOW, w*2, h*4)
                self.CLIENT.start(ADDR, SOCK, self.USERNAME, hex(get_random_n_digit_int(9)))
            else:
                print("General chat submit")
                usr_input = self.ent_text_input.get()
                textr = self.lbl_text_display.cget("text") + usr_input
                self.ent_text_input.delete(0, tk.END)
                self.lbl_text_display.configure(text=textr)
          
        self.lbl_text_display.pack()
        self.frm_text_display.pack()
        
        self.lbl_text_dscrptn.pack()
        self.frm_text_dscrptn.pack()
        
        self.ent_text_input.pack()
        self.frm_text_input.pack()
        
        
        self.btn_submit.pack()
        self.frm_submit.pack(side=tk.LEFT)
        
        self.frm_main.pack(padx=50, pady=50)
        
        self.set_geometry(WINDOW, w, h)
        
        self.btn_submit.bind("<Button-1>", handle_click)
        print("Messenger_GUI.py: bottom of start")
if __name__ == '__main__':
    gui = MessengerGUI()
    
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ADDR = (HOST, PORT)
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    WINDOW = tk.Tk()
    gui.start(ADDR, SOCK, WINDOW)
    WINDOW.mainloop()
