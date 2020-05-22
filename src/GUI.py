from tkinter import *
from tkinter import messagebox

class SignUp(Frame):
    pass

class Application(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.Creat_widgets()

    def Creat_widgets(self): # interface
        self.tl=t.title("CaVid-G4 App") # title
        self.frame=t.geometry("300x140+500+180")
        t.resizable(width=False, height=False)

        self.lb=Label(t,text="--Well com to CaVidG4--") # <h1> lable
        self.lb.pack()

        self.lb1 = Label(t,text="Sign in Account") # <h2> sublable
        self.lb1.pack()

        self.lb_acc=Label(t,text="account: ") # <p> account
        self.lb_acc.pack()
        self.lb_acc.place(x=20,y=50)

        self.en_acc=Entry(t) # Entry account
        self.en_acc.pack()
        self.en_acc.place(x=77,y=50)

        self.lb_pass=Label(t,text="password: ") # <p> password
        self.lb_pass.pack()
        self.lb_pass.place(x=20,y=76)

        self.en_pass = Entry(t,show="*")  # Entry password
        self.en_pass.pack()
        self.en_pass.place(x=77, y=76)

        self.bt_login=Button(t,text="Log in",font=(13),height=2,command=self.Login) # Button Login
        self.bt_login.pack()
        self.bt_login.place(x=220,y=46)

        self.bt_signup = Button(t,text="Sign up",command=self.SigUp) # Button Sign up
        self.bt_signup.pack()
        self.bt_signup.place(x=77, y=100)

    def SigUp(self): # Process Sign Up

        self.top=Toplevel(t)
        self.frame = self.top.geometry("300x180+450+180")
        self.top.resizable(width=False, height=False)
        self.lb2 = Label(self.top, text="--Register--", font=("", 14)).pack()

        self.lb1_acc = Label(self.top, text="phone: ")  # <p> account
        self.lb1_acc.pack()
        self.lb1_acc.place(x=20, y=50)

        self.en1_acc = Entry(self.top)  # Entry account
        self.en1_acc.pack()
        self.en1_acc.place(x=77, y=50)
        self.en1_acc.focus()

        self.lb1_pass = Label(self.top, text="password: ")  # <p> password
        self.lb1_pass.pack()
        self.lb1_pass.place(x=20, y=76)

        self.en1_pass = Entry(self.top,show="*")  # Entry password
        self.en1_pass.pack()
        self.en1_pass.place(x=77, y=76)

        self.lb1_conf = Label(self.top, text="confirm: ")  # <p> confirm
        self.lb1_conf.pack()
        self.lb1_conf.place(x=20, y=100)

        self.en1_conf = Entry(self.top,show="*")  # Entry confirm
        self.en1_conf.pack()
        self.en1_conf.place(x=77, y=100)

        self.lb1_phone = Label(self.top, text="name: ")  # <p> confirm
        self.lb1_phone.pack()
        self.lb1_phone.place(x=20, y=126)

        self.en1_phone = Entry(self.top)  # Entry confirm
        self.en1_phone.pack()
        self.en1_phone.place(x=77, y=126)

        self.bt_login = Button(self.top, text="Submit", font=(13), height=2,command=self.Storage)  # Button Submit
        self.bt_login.pack()
        self.bt_login.place(x=220, y=70)

    def Interface_Call(self): # Process Login
        t.withdraw() # hidden main window
        self.lg=Toplevel(t)
        self.frame = self.lg.geometry("300x140+500+180")
        self.lg.resizable(width=False, height=False)
        self.lb = Label(self.lg, text="CaVid-G4 App", font=("", 14)).pack()
        self.lb = Label(self.lg, text="user: {}".format(self.name), font=("", 13)).pack()

        self.bt_logout = Button(self.lg, text="Logout", height=3, width=7, command=self.LogOut)
        self.bt_logout.pack()
        self.bt_logout.place(x=240,y=85)

        self.bt_exit = Button(self.lg, text="Exit", height=3, width=7,command=t.destroy)
        self.bt_exit.pack()
        self.bt_exit.place(y=85)

        self.bt_call = Button(self.lg, text="Call", height=3,width=7)  ############################################ Button Call
        self.bt_call.pack()
        self.bt_call.place(x=120,y=85)

    def LogOut(self): # Process Logout
        t.deiconify() # show main window again
        self.lg.destroy()

#-------------------------------Store and process data------------------------------------------------------------------

    def Storage(self): # Store data at a Repository.txt file
        infor=self.en1_acc.get()+" " + self.en1_pass.get() + " " + self.en1_phone.get()+"\n"
        f=open("Repository.txt","a")
        f.writelines(infor)
        f.close()
        messagebox.showinfo("Notification","Register Access!")
        self.top.destroy()

    def Login(self):
        data=[]
        f=open("Repository.txt","r")
        while True:
            infor=f.readline()
            if(infor==""):
                messagebox.showwarning("Warring!","Account does not exist")
                break
            else:
                data=infor.split()
                self.name = data[2]
                if(self.en_acc.get()==data[0] and self.en_pass.get()==data[1]):
                    self.Interface_Call()
                    break
                elif(self.en_acc.get()!=data[0] or self.en_pass.get()!=data[1]):
                    messagebox.showerror("Error!", "incorrect account or password")
                    break
        f.close()

if __name__=="__main__":
    t=Tk()
    app=Application(t)
    app.mainloop()
