import tkinter
from tkinter import *
from tkinter import messagebox


root=Tk()
root.title("Tic Tac Toe 2.0")
root.geometry("450x700")
clicked=True
count=0
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

#check if someone win
def check_if_win():
    global winner
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
    if count==27 and winner==False:
        messagebox.showinfo("Tic Tac Toe 2.0","It's a tie!\nNobody wins the game!")
        disable_all_buttons()


# when click, what should the program do
def button_click(b):
    global clicked, count
    pass

name_label=tkinter.Label(root, text="Let's play the game!")
name_label.grid(row=0,column=2)
b1=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b1))
b2=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b2))
b3=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b3))
b4=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b4))
b5=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b5))
b6=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b6))
b7=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b7))
b8=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b8))
b9=Button(root,text=" ",font=("Times",20),height=3,width=6,bg="SystemButtonFace",command=lambda : button_click(b9))

b1.grid(row=1,column=1)
b2.grid(row=1,column=2)
b3.grid(row=1,column=3)

b4.grid(row=2,column=1)
b5.grid(row=2,column=2)
b6.grid(row=2,column=3)

b7.grid(row=3,column=1)
b8.grid(row=3,column=2)
b9.grid(row=3,column=3)


root.mainloop()


