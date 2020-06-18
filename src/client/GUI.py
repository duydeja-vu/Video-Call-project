import sys
sys.path.append("..")

from tkinter import *
from tkinter import messagebox
from multiprocessing import Process, Queue
from utils import config
from socket import *
import pickle
import cv2
import numpy as np
import clientVideo




class Application(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.Creat_widgets()
        self.queue_GUI_Socket = Queue()
        self.main_socket = None
        self.is_first_access = True
        self.my_username = ""
        self.my_password = ""


    def Creat_widgets(self): # interface
        self.tl=t.title("Video Conference") # title
        self.frame=t.geometry("300x140+500+180")
        t.resizable(width=False, height=False)

        self.lb=Label(t,text="--Well com to Video Conference--") # <h1> lable
        self.lb.pack()

        self.lb1 = Label(t,text="Sign in Account") # <h2> sublable
        self.lb1.pack()

        self.lb_acc=Label(t,text="account: ") # <p> account
        self.lb_acc.pack()
        self.lb_acc.place(x=10,y=50)

        self.en_acc=Entry(t) # Entry account
        self.en_acc.pack()
        self.en_acc.place(x=77,y=50)

        self.lb_pass=Label(t,text="password: ") # <p> password
        self.lb_pass.pack()
        self.lb_pass.place(x=10,y=76)

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

        self.lb1_acc = Label(self.top, text="user name: ")  # <p> account
        self.lb1_acc.pack()
        self.lb1_acc.place(x=10, y=50)

        self.en1_acc = Entry(self.top)  # Entry account
        self.en1_acc.pack()
        self.en1_acc.place(x=77, y=50)
        self.en1_acc.focus()

        self.lb1_pass = Label(self.top, text="password: ")  # <p> password
        self.lb1_pass.pack()
        self.lb1_pass.place(x=10, y=76)

        self.en1_pass = Entry(self.top,show="*")  # Entry password
        self.en1_pass.pack()
        self.en1_pass.place(x=77, y=76)

        self.lb1_conf = Label(self.top, text="confirm: ")  # <p> confirm
        self.lb1_conf.pack()
        self.lb1_conf.place(x=10, y=100)

        self.en1_conf = Entry(self.top,show="*")  # Entry confirm
        self.en1_conf.pack()
        self.en1_conf.place(x=77, y=100)

        self.bt_login = Button(self.top, text="Submit", font=(13), height=2,command=self.Register)  # Button Submit
        self.bt_login.pack()
        self.bt_login.place(x=100, y=125)

    def Interface_Call(self): # Process Login
        t.withdraw() # hidden main window
        self.lg=Toplevel(t)
        self.frame = self.lg.geometry("300x140+500+180")
        self.lg.resizable(width=False, height=False)
        Label(self.lg, text="CaVid-G4 App", font=("", 14)).pack()

        self.bt_logout = Button(self.lg, text="Logout", height=3, width=7, command=self.LogOut)
        self.bt_logout.pack()
        self.bt_logout.place(x=240,y=85)
        clientVideo.StartVideoCall()


       
        # self.bt_exit = Button(self.lg, text="Exit", height=3, width=7,command=t.destroy)
        # self.bt_exit.pack()
        # self.bt_exit.place(y=85)

    def StartVideoCall(self):
        # cap = cv2.VideoCapture(0)
        # while True:
        #     _, frame = cap.read()
        #     cv2.imshow(self.my_username, frame)
            
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # cap.release()
        # cv2.destroyAllWindows()
        # return
        # video_call_process = Process(target=clientMedia.StartVideoCall())
        # video_call_process.start()
        clientVideo.StartVideoCall()
    


    def LogOut(self):
        logout_data = []
        logout_data.append("Exit")
        logout_data.append(self.my_username)
        logout_data.append(self.my_password)
        self.queue_GUI_Socket.put(logout_data)
        self.StartMainSocket()
        t.deiconify() # show main window again
        self.lg.destroy()


    def Register(self): 
        register_data = []
        register_data.append("Register")
        register_data.append(self.en1_acc.get())
        register_data.append(self.en1_pass.get())
        self.queue_GUI_Socket.put(register_data)
        self.StartMainSocket()
       

    def Login(self):
        login_data=[]
        login_data.append("Login")
        login_data.append(self.en_acc.get())
        login_data.append(self.en_pass.get())
        self.queue_GUI_Socket.put(login_data)
        

        self.StartMainSocket()
       

    def StartMainSocket(self):
        if self.is_first_access == True:
            self.main_socket = socket(AF_INET, SOCK_STREAM)
            print(self.main_socket)
            self.main_socket.connect((config.HOST, config.MAIN_PORT))
            self.is_first_access = False
        
        user_data = []
        if self.queue_GUI_Socket.qsize() != 0:
            user_data = self.queue_GUI_Socket.get()
            print("user data", user_data)
        
        if user_data[0] == "Register" or user_data[0] == "Login":
            self.my_username = user_data[1]
            self.my_password = user_data[2]

        send_mess = str(user_data)
        print("After 156")
        self.main_socket.send(send_mess.encode('utf-8'))
        print("After 158")
        receive_mess = self.main_socket.recv(config.BUFFSIZE)
        receive_mess =  receive_mess.decode('utf-8')
        if receive_mess == "200_OK":
            print("Logined")
            self.Interface_Call()
        elif receive_mess == "500_NOTOK":
            print("Wrong user name or password")
        elif receive_mess == "EXITOK":
            print("EXIT")
            return
        


if __name__=="__main__":
    t=Tk()
    app=Application(t)
    app.mainloop()
