#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
from chat_utils import *
from PIL import ImageTk,Image
import json
import base64
#import game_tic_tac_toe as game
# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.52,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

       

        #m------------------------------
        # create a image Button
        self.buttonImage = Button(self.labelBottom,
                                text="Image",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.imageButton(self.entryMsg.get()))

        self.buttonImage.place(relx=0.55,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
        #m------------------------------

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages

    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    #m------------------------------
    def imageButton(self, msg):
        self.my_msg = msg
        
        self.imageviewer = Toplevel()
        self.imageviewer.title('Image Viewer')
        self.imageviewer.iconbitmap('desktop/ICS-final/ICS-final/chat_system_gui')

        global my_image
        self.imageviewer.filename = filedialog.askopenfilename(initialdir="/images", title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
        #my_label = Label(self.imageviewer, text=self.imageviewer.filename)
        my_image = ImageTk.PhotoImage(Image.open(self.imageviewer.filename))
        my_image_label = Label(self.imageviewer,image=my_image)
        my_image_label.grid(row=0, column=0, columnspan=3, sticky=W+E)
        #self.sendButton(my_image_label)

        image_name = self.imageviewer.filename.split('/')[-1]
        #with open(self.imageviewer.filename, "rb") as image2string:
            #my_image_code = base64.b64encode(image2string.read()).decode('utf8')

        self.ImageMsg = Label(self.imageviewer,
                            text = 'Message',
                            font="Helvetica 13")
        self.ImageMsg.grid(row=1, column=0, columnspan=1, sticky=W+E)
        self.entryImage = Entry(self.imageviewer,
                            bg="#2C3E50",
                            fg="#EAECEE",
                            font="Helvetica 13")
        #self.entryImage.focus()
        self.entryImage.grid(row=1, column=1, columnspan=2, sticky=W+E)
        self.entryImage.insert(0,'(' + image_name + ')')
        self.buttonSendImage = Button(self.imageviewer,
                                text="Send image",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendImage(image_name,self.imageviewer.filename,self.entryImage.get()))
                                #command=lambda: self.sendImage(image_name,my_image_code,self.entryImage.get()))

        self.buttonSendImage.grid(row=3, column=0, columnspan=3, sticky=W+E)
                       
    def sendImage(self,image_name,image_filename,msg): 
        #image_name = image_filename.split('/')[-1]
        with open(image_filename, "rb") as image2string:
            my_image_code = base64.b64encode(image2string.read()).decode('utf8')
        #---------------------------------
    #def sendImage(self,image_name,my_image_code,msg):
        self.my_msg = msg
        self.sm.my_image = [image_name, my_image_code]
        # print(msg)
        self.entryImage.delete(0, END)
        self.sendButton(msg)
        #self.textCons.config(state=NORMAL)
        #self.textCons.insert(END, msg + "\n")
        #self.textCons.config(state=DISABLED)
        #self.textCons.see(END)
        #msg = json.dumps({"action": "exchange", "message" : my_image})
        #self.send(msg)
        #response = json.loads(self.recv())
        
    
    def saveImage(self,peer_image,location = 'peer_images/'):
        image = peer_image[1].encode('utf8')
        f = open(location+peer_image[0],'wb')
        f.write(base64.b64decode(image))
        #f.write(base64.b64decode(peer_image[1]))
        f.close()
        self.imageviewer2 = Toplevel()
        self.imageviewer2.title('Image Viewer')
        self.imageviewer2.iconbitmap('desktop/ICS-final/ICS-final/chat_system_gui')
        global my_image
        my_image = ImageTk.PhotoImage(Image.open(location+peer_image[0]))
        my_image_label = Label(self.imageviewer2,image=my_image).pack()
        

    #m------------------------------

    def proc(self):
        # print(self.msg)
        while True:
            if self.sm.state != S_GAMING:
                read, write, error = select.select([self.socket], [], [], 0)
                peer_msg = []
                # print(self.msg)
                if self.socket in read:
                    peer_msg = self.recv()
                if len(self.my_msg) > 0 or len(peer_msg) > 0:
                    # print(self.system_msg)
                    self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                    #try:
                        #self.system_msg = self.system_msg[0]
                        #print(self.system_msg)
                        #game.main(self.sm.game_role,self.sm.me,socket=self.s)
                    #except:
                        #pass
                    self.my_msg = ""
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, self.system_msg + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    self.sm.my_image = []
                    #downloads image
                    if len(self.sm.peer_image) > 0:
                        self.saveImage(self.sm.peer_image)
                        self.sm.peer_image = []
                        #self.openImage()
                    #peer_msg = json.loads(peer_msg)
                    #if peer_msg['action'] == 'game':

                
                    

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
