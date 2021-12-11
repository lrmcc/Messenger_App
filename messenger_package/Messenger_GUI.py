#!/usr/bin/env python3

import tkinter as tk

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


def main():
    window = tk.Tk()
    
    window.title('Messenger_App')
        
    frm_login_page = tk.Frame(master=window, width=100, height=100)
    
    lbl_login_page = tk.Label(master=frm_login_page, text="Enter username to join:")
    lbl_login_page.pack()
        
    ent_login_page = tk.Entry(master=frm_login_page)
    ent_login_page.pack()
    
    btn_login_page = tk.Button(
        master=frm_login_page,
        text="Submit",
        width=17,
        height=5,
        bg="red",
        fg="black",
        )
    btn_login_page.pack()
    
    frm_login_page.pack(padx=50, pady=50)


    w = 300 
    h = 200 
    
    x_coord = (window.winfo_screenwidth()/2) - (w/2)
    y_coord = ((window.winfo_screenheight()/2) - (h/2)) * .5
    
    window.geometry('%dx%d+%d+%d' % (w, h, x_coord, y_coord))

    window.mainloop()


if __name__ == '__main__':
    main()
