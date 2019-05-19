from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Frame, Label, Entry, Combobox, Button, Checkbutton, Radiobutton
from final import *

root = Tk()
root.geometry("460x180+300+300")
status = StringVar()
Label(root, textvariable=status, border=1, relief=SUNKEN, anchor=W).pack(side=BOTTOM, fill=X)
status.set("B1606868 - Thanh Bảo | Copyleft")


class UI(Frame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.master.title("Niên Luận")
        self.pack(fill=BOTH, expand=True)
        i = IntVar()
        i=1

        fr0 = Frame(self)
        fr0.pack(fill = X)
        llbl = Label(fr0, text= "TOOL 4 IN 1!", foreground = "red")
        labelfont = ('times', 20, 'bold')
        llbl.config(font=labelfont)          
        llbl.pack()
        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Find what:", width = 9)
        lbl1.pack(side=LEFT, padx =5, pady=5)
        entry1 = Entry(frame1, width = 31)
        entry1.pack(fill =X, padx = 5)

        

        frame2 = Frame(self)
        frame2.pack(fill=X)


        lbl2 = Label(frame2, text="Number(s):", width=10)
        lbl2.pack(side=LEFT, padx=5, pady=5)
        
        entry2 = Entry(frame2, width = 7)
        entry2.pack(side = LEFT, padx=5)
        lbl3 = Label(frame2, text="(Amount of videos downloaded can be less)")
        labelfont = ('times', 10, 'bold')
        lbl3.config(font=labelfont)       
        lbl3.pack(side=LEFT, padx = 5, pady=5)
        
        frame3 = Frame(self, height = 30)
        frame3.pack(fill=X)
        lbl3 = Label(frame3, text="CREATE FILE SUB: ", width=15)
        lbl3.pack(side=LEFT, padx=5, pady=5)
        idsub = ["YES","NO"]
        combo1 = Combobox(frame3, values = idsub, width = 5)
        combo1.set("NO")
        combo1.pack(side = LEFT, padx = 5)

        lbl2 = Label(frame3, text="Language:", width = 10)
        lbl2.pack(side=LEFT, padx = 5, pady=5)
        
        combo = Combobox(frame3, values = ["Tiếng Việt","English"], width = 10)
        combo.set("Tiếng Việt")
        combo.pack(side = LEFT)
        



        frame4 = Frame(self, height = 40, border = 1)
        frame4.pack(fill=X)
        btn1 = Button(frame4, text= "Download only", width = 20, command = lambda: downloadOnly(entry1.get(), entry2.get()))        
        btn1.pack(side = LEFT,anchor = S, padx = 15)
        btn3 = Button(frame4, text= "4 in 1", width = 28, command = lambda: mainP(entry1.get(), entry2.get(), combo.get(),combo1.get()))        
        btn3.pack(side = LEFT,anchor=E, padx = 2)
        

def mainP(searchkey, stop, lg, isSub) :
    if (searchkey == "" and stop == ""):
        # MessageBox 
    
        messagebox.showerror("ERROR", "Please fill full information!")
    else: 
        if (isSub == "YES"):
        
            id = ["Tiếng Việt","English"]
            lgs = ["vi-VN", "en-US"]
            mainprocess(searchkey, stop, lgs[id.index(lg)])
            messagebox.showinfo("Process", "Done")
        else:
            mainprocessWithoutSub(searchkey, stop)
            messagebox.showinfo("Process", "Done")


def downloadOnly(search, stop):
    if (search== "" and stop==""):
        # MessageBox 
        messagebox.showerror("ERROR", "Please fill full information!")
        
    else:
         
        Justdown(search, stop)
        messagebox.showinfo("Process", "Done")



def main():

    
    app = UI()

    root.mainloop()


if __name__ == '__main__':
    main()