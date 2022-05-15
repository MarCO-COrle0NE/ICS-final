from cgitb import enable
import tkinter
from tkinter import *
from tkinter import messagebox
from chat_utils import *
import json
import select

#class Toplevel1(Toplevel):
    #def init(self):
        #super().__init__()
    #def destroy1(self):
        #self.destroy()


def main(sm,socket=None):
    global root
    root=Toplevel()
    root.title("Tic Tac Toe 2.0")
    root.geometry("450x700")
    global clicked, count,dict_x,dict_o,flg
    clicked,flg=True,False
    role = sm.game_role
    me = sm.me
    #my_turn = True
    count=0
    # dict to record the remaining chess pieces
    dict_x={"x":3,"xx":3,"xxx":3}
    dict_o={"o":3,"oo":3,"ooo":3}
    # Button里没有text时，选完piece之后的操作


    def quit():
        try:
            root.destroy()
            sm.state = S_LOGGEDIN
            msg = json.dumps({"action" :"game", "from": "[" + me + "]" , "move":"quit"})
            mysend(socket,msg)
            #msg = json.dumps({"action":"exchange","from":"[" + me + "]" , "message" : "bye","image":''})
            #mysend(socket,msg)
            
        except:
            pass

    def move_send(move):
        msg = json.dumps({"action":"game", "from":"[" + me + "]", "move":move})
        mysend(socket, msg)
    
    def move_recv():
        #read, write, error = select.select([socket], [], [], 0)
        #peer_msg = []
        #print(self.msg)
        #if socket in read:
        peer_msg = myrecv(socket)
        
        peer_msg = json.loads(peer_msg)
        print(peer_msg)
        if peer_msg["move"] == "quit":
                quit()
                print('quit!')
                return None
        while len(peer_msg) <= 0 or peer_msg['action'] != 'game':
            peer_msg = myrecv(socket)
            peer_msg = json.loads(peer_msg)
            print(peer_msg)
            if peer_msg["move"] == "quit":
                quit()
                print('quit!')
                return None
                
                #print(peer_msg)
                
        peer_chess = peer_msg['move'][1]
        peer_button = lb[peer_msg['move'][0]]
        peer_msg = ''
        peer_move(peer_chess,peer_button)

    def peer_move(peer_chess,peer_button):
        global clicked,count
        peer_button["text"] = ""
        if role == 'x':
            if peer_chess == 1:
                peer_button["text"] = "o"
            elif peer_chess == 2:
                peer_button["text"] = "oo"
            elif peer_chess == 3:
                peer_button["text"] = "ooo"
        else:
            if peer_chess == 1:
                peer_button["text"] = "x"
            elif peer_chess == 2:
                peer_button["text"] = "xx"
            elif peer_chess == 3:
                peer_button["text"] = "xxx"
        clicked = not clicked
        switch_turn()
        count += 1
        check_if_win()
        if winner:
            messagebox.showinfo("Game over!", "Congratulation! x wins!")

    def switch_turn():
        global my_turn,clicked
        if clicked:
            if role == 'x':
                turn_label['text'] = "It's x's turn"
                
                my_turn = True
                enable_all_buttons()
            else:
                turn_label['text'] = "It's x's turn"
                
                my_turn = False
                disable_all_buttons()
                move_recv()
                
        else:
            if role == 'x':
                turn_label['text'] = "It's o's turn"
                
                my_turn = False
                disable_all_buttons()
                move_recv()
                
            else:
                turn_label['text'] = "It's o's turn"
                
                my_turn = True
                enable_all_buttons()
    #switch_turn()
    def root1_b_small_click(root1_b,b):
        global clicked,winner,count,root1
        #global clicked,winner,count
        if dict_x["x"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root1_b.config(state=DISABLED)
            b["text"] = "x"
            dict_x["x"] -= 1
            if my_turn:
                move_send([lb.index(b),1])
            clicked = False
            root1.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
    def root1_b_medium_click(root1_b,b):
        global clicked,winner,count,root1
        if dict_x["xx"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root1_b.config(state=DISABLED)
            b["text"] = "xx"
            dict_x["xx"] -= 1
            if my_turn:
                move_send([lb.index(b),2])
            clicked = False
            root1.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
    def root1_b_big_click(root1_b,b):
        global clicked,winner,count,root1
        if dict_x["xxx"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root1_b.config(state=DISABLED)
            b["text"] = "xxx"
            dict_x["xxx"] -= 1
            if my_turn:
                move_send([lb.index(b),3])
            clicked = False
            root1.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
    def root2_b_small_click(root2_b,b):
        global clicked,winner,count,root2
        if dict_o["o"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root2_b.config(state=DISABLED)
            b["text"] = "o"
            dict_o["o"] -= 1
            if my_turn:
                move_send([lb.index(b),1])
            clicked = True
            root2.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把x变成player的名字
    def root2_b_medium_click(root2_b,b):
        global clicked,winner,count,root2
        if dict_o["oo"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root2_b.config(state=DISABLED)
            b["text"] = "oo"
            dict_o["oo"] -= 1
            if my_turn:
                move_send([lb.index(b),2])
            clicked = True
            root2.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把o变成player的名字
    def root2_b_big_click(root2_b,b):
        global clicked,winner,count,root2
        if dict_o["ooo"]==0:
            messagebox.showwarning("You can't choose this button!","You don't have this piece!\nChoose another one!")
        else:
            root2_b.config(state=DISABLED)
            b["text"] = "ooo"
            dict_o["ooo"] -= 1
            if my_turn:
                move_send([lb.index(b),3])
            clicked = True
            root2.destroy()
            switch_turn()
            count += 1
            check_if_win()
            if winner:
                messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把o变成player的名字




    # Disable all buttons when game ends
    def disable_all_buttons():
        b1.config(state=DISABLED)
        b2.config(state=DISABLED)
        b3.config(state=DISABLED)
        b4.config(state=DISABLED)
        b5.config(state=DISABLED)
        b6.config(state=DISABLED)
        b7.config(state=DISABLED)
        b8.config(state=DISABLED)
        b9.config(state=DISABLED)
    
    def enable_all_buttons():
        b1.config(state=NORMAL)
        b2.config(state=NORMAL)
        b3.config(state=NORMAL)
        b4.config(state=NORMAL)
        b5.config(state=NORMAL)
        b6.config(state=NORMAL)
        b7.config(state=NORMAL)
        b8.config(state=NORMAL)
        b9.config(state=NORMAL)

    #check if someone win
    def check_if_win():
        global winner,count
        winner=False
        index_x_b1,index_x_b2,index_x_b3=b1["text"].find("x"),b2["text"].find("x"),b3["text"].find("x")
        index_x_b4, index_x_b5, index_x_b6 = b4["text"].find("x"), b5["text"].find("x"), b6["text"].find("x")
        index_x_b7, index_x_b8, index_x_b9= b7["text"].find("x"), b8["text"].find("x"), b9["text"].find("x")
        index_o_b1, index_o_b2, index_o_b3 = b1["text"].find("o"), b2["text"].find("o"), b3["text"].find("o")
        index_o_b4, index_o_b5, index_o_b6 = b4["text"].find("o"), b5["text"].find("o"), b6["text"].find("o")
        index_o_b7, index_o_b8, index_o_b9 = b7["text"].find("o"), b8["text"].find("o"), b9["text"].find("o")
        if index_x_b1!=-1 and index_x_b2!=-1 and index_x_b3!=-1:
            b1.config(bg="green")
            b2.config(bg="green")
            b3.config(bg="green")
            winner=True
            count+=1
            disable_all_buttons()
            # may show win message
        elif index_o_b1!=-1 and index_o_b2!=-1 and index_o_b3!=-1:
            b1.config(bg="green")
            b2.config(bg="green")
            b3.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
            # may show win message
        elif index_x_b4!=-1 and index_x_b5!=-1 and index_x_b6!=-1:
            b4.config(bg="green")
            b5.config(bg="green")
            b6.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b4!=-1 and index_o_b5!=-1 and index_o_b6!=-1:
            b4.config(bg="green")
            b5.config(bg="green")
            b6.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b7!=-1 and index_x_b8!=-1 and index_x_b9!=-1:
            b7.config(bg="green")
            b8.config(bg="green")
            b9.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b7!=-1 and index_o_b8!=-1 and index_o_b9!=-1:
            b7.config(bg="green")
            b8.config(bg="green")
            b9.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b1!=-1 and index_x_b4!=-1 and index_x_b7!=-1:
            b1.config(bg="green")
            b4.config(bg="green")
            b7.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b1!=-1 and index_o_b4!=-1 and index_o_b7!=-1:
            b1.config(bg="green")
            b4.config(bg="green")
            b7.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b2!=-1 and index_x_b5!=-1 and index_x_b8!=-1:
            b2.config(bg="green")
            b5.config(bg="green")
            b8.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b2!=-1 and index_o_b5!=-1 and index_o_b8!=-1:
            b2.config(bg="green")
            b5.config(bg="green")
            b8.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b3!=-1 and index_x_b6!=-1 and index_x_b9!=-1:
            b3.config(bg="green")
            b6.config(bg="green")
            b9.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b3!=-1 and index_o_b6!=-1 and index_o_b9!=-1:
            b3.config(bg="green")
            b6.config(bg="green")
            b9.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b1!=-1 and index_x_b5!=-1 and index_x_b9!=-1:
            b1.config(bg="green")
            b5.config(bg="green")
            b9.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b1!=-1 and index_o_b5!=-1 and index_o_b9!=-1:
            b1.config(bg="green")
            b5.config(bg="green")
            b9.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif index_x_b3!=-1 and index_x_b5!=-1 and index_x_b7!=-1:
            b3.config(bg="green")
            b5.config(bg="green")
            b7.config(bg="green")
            winner=True
            count += 1
            disable_all_buttons()
        elif index_o_b3!=-1 and index_o_b5!=-1 and index_o_b7!=-1:
            b3.config(bg="green")
            b5.config(bg="green")
            b7.config(bg="green")
            winner = True
            count += 1
            disable_all_buttons()
        elif count==27 and winner==False:# tie 的条件有问题
            messagebox.showinfo("Tic Tac Toe 2.0","It's a tie!\nNobody wins the game!")
            disable_all_buttons()
        elif flg:
            messagebox.showinfo("Tic Tac Toe 2.0","It's a tie!\nNobody wins the game!")
            disable_all_buttons()
            quit()
        if winner:
            quit()

    # when click, what should the program do
    # x start first
    def button_click(b):
        global clicked, count,dict_o,dict_x
        # 已有最大的棋但还是点了
        if b["text"]=="ooo":
            messagebox.showwarning("You can't put your piece here!","You can't put any piece here\nbecause \'ooo\' is the largest piece!\nPlease choose another place!")
            b.config(state=DISABLED)
        elif b["text"]=="xxx":
            messagebox.showwarning("You can't put your piece here!",
                                   "You can't put any piece here\nbecause \'xxx\' is the largest piece!\n\
                                   Please choose another place!")
            b.config(state=DISABLED)
        # 有o或x在button
        elif clicked==True and len(b["text"])==1:
            if dict_x["xx"]==0 and dict_x["xxx"]!=0:
                messagebox.showinfo("You only have one choice!","The big piece will be set here.")
                b["text"]="xxx"
                dict_x["xxx"]-=1
                if my_turn:
                    move_send([lb.index(b),3])
                clicked=False
                switch_turn()
                count+=1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
            elif dict_x["xxx"]==0 and dict_x["xx"]!=0:
                messagebox.showinfo("You only have one choice!", "The medium piece will be set here.")
                b["text"] = "xx"
                dict_x["xx"] -= 1
                if my_turn:
                    move_send([lb.index(b),2])
                clicked = False
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
            elif dict_x["xxx"]==0 and dict_x["xx"]==0:
                messagebox.showwarning("You have no choice!", "You can't put any piece here\n\
                                                           because you don't have suitable piece!\n\
                                                           Please choose another place!")
                flg=True
            else:
                result=messagebox.askokcancel("which piece would you choose?","If you choose big piece, please click \'OK\' Button.\"\
                                                                   \n If you choose medium piece, please click \'Cancel\' Button.")
                if result:
                    b["text"]="xxx"
                    dict_x["xxx"]-=1
                    if my_turn:
                        move_send([lb.index(b),3])
                else:
                    b["text"]="xx"
                    dict_x["xx"]-=1
                    if my_turn:
                        move_send([lb.index(b),2])
                clicked=False
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!","Congratulation! x wins!")# 可能要把x变成player的名字
        elif clicked==False and len(b["text"])==1:
            if dict_o["oo"]==0 and dict_o["ooo"]!=0:
                messagebox.showinfo("You only have one choice!","The big piece will be set here.")
                b["text"]="ooo"
                dict_o["ooo"]-=1
                if my_turn:
                    move_send([lb.index(b),3])
                clicked=True
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把o变成player的名字
            elif dict_o["ooo"]==0 and dict_o["oo"]!=0:
                messagebox.showinfo("You only have one choice!", "The medium piece will be set here.")
                b["text"] = "oo"
                dict_o["oo"] -= 1
                if my_turn:
                    move_send([lb.index(b),2])
                clicked = True
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把o变成player的名字
            elif dict_o["ooo"]==0 and dict_o["oo"]==0:
                messagebox.showwarning("You have no choice!", "You can't put any piece here\n\
                                                           because you don't have suitable piece!\n\
                                                           Please choose another place!")
                flg=True
            else:
                result = messagebox.askokcancel("which piece would you choose?", "If you choose big piece, please click \'OK\' Button.\"\
                                                                           \n If you choose medium piece, please click \'Cancel\' Button.")
                if result:
                    b["text"]="ooo"
                    dict_o["ooo"]-=1
                    if my_turn:
                        move_send([lb.index(b),3])
                else:
                    b["text"]="oo"
                    dict_o["oo"]-=1
                    if my_turn:
                        move_send([lb.index(b),2])
                clicked=True
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! o wins!") #换player名字
        # 有 “oo”和“xx”在button
        elif clicked==True and len(b["text"])==2:
            if dict_x["xxx"]!=0:
                messagebox.showinfo("You only have one choice!","The big piece will be set here.")
                b["text"]="xxx"
                dict_x["xxx"]-=1
                if my_turn:
                    move_send([lb.index(b),3])
                clicked=False
                switch_turn()
                count += 1
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! x wins!")  # 可能要把x变成player的名字
            elif dict_x["xxx"]==0:
                messagebox.showwarning("You have no choice!"," You can't put any piece here\n\
                                                                       because you don't have suitable piece!\n\
                                                                       Please choose another place!")
                flg=True
        elif clicked==False and len(b["text"])==2:
            if dict_o["ooo"]!=0:
                messagebox.showinfo("You only have one choice!"," The big piece will be set here.")
                b["text"]="ooo"
                dict_o["ooo"]-=1
                if my_turn:
                    move_send([lb.index(b),3])
                clicked=True
                switch_turn()
                count += 1
                flg=False
                check_if_win()
                if winner:
                    messagebox.showinfo("Game over!", "Congratulation! o wins!")  # 可能要把o变成player的名字
            elif dict_o["ooo"]==0:
                messagebox.showwarning("You have no choice!", "You can't put any piece here\n\
                                                                       because you don't have suitable piece!\n\
                                                                       Please choose another place!")
                flg=True
        # Button里是空的
        elif clicked==True and b["text"]=="":
            global root1
            root1=Toplevel()
            root1.title("Choose one piece!")
            root1_name_label = tkinter.Label(root1, text="Click the corresponding Button of the piece you want to choose!")
            root1_name_label1=tkinter.Label(root1, text="Please close the window after the selected piece is shown!")
            root1_name_label.grid(row=0,column=1)
            root1_name_label1.grid(row=1,column=1)

            b_small=Button(root1,text="x",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda: root1_b_small_click(b_small,b))
            b_medium=Button(root1,text="xx",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : root1_b_medium_click(b_medium,b))
            b_big=Button(root1,text="xxx",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : root1_b_big_click(b_big,b))

            b_small.grid(row=2, column=0)
            b_medium.grid(row=2, column=1)
            b_big.grid(row=2, column=2)
        elif clicked==False and b["text"]=='':
            global root2
            root2=Toplevel()
            root2.title("Choose one piece!")
            root2_name_label = tkinter.Label(root2, text="Click the corresponding Button of the piece you want to choose!")
            root2_name_label1=tkinter.Label(root2, text="Please close the window after the selected piece is shown!")
            root2_name_label.grid(row=0,column=1)
            root2_name_label1.grid(row=1,column=1)

            b_small=Button(root2,text='o',font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda :root2_b_small_click(b_small,b))
            b_medium=Button(root2,text="oo",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : root2_b_medium_click(b_medium,b))
            b_big=Button(root2,text="ooo",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : root2_b_big_click(b_big,b))

            b_small.grid(row=2, column=0)
            b_medium.grid(row=2, column=1)
            b_big.grid(row=2, column=2)
        check_if_win()

    name_label=tkinter.Label(root, text="Let's play the game! You're %s" % role)
    name_label.grid(row=0,column=2)
    

    b1=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b1))
    b2=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b2))
    b3=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b3))
    b4=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b4))
    b5=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b5))
    b6=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b6))
    b7=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b7))
    b8=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b8))
    b9=Button(root,text="",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b9))
    lb = [0,b1,b2,b3,b4,b5,b6,b7,b8,b9]
    turn_label = tkinter.Label(root, text="")
    #switch_turn()
    turn_label.grid(row=1,column=2)

    b1.grid(row=2,column=1)
    b2.grid(row=2,column=2)
    b3.grid(row=2,column=3)

    b4.grid(row=3,column=1)
    b5.grid(row=3,column=2)
    b6.grid(row=3,column=3)

    b7.grid(row=4,column=1)
    b8.grid(row=4,column=2)
    b9.grid(row=4,column=3)

    switch_turn()
    #root.mainloop()
if __name__=="__main__":
    main()




