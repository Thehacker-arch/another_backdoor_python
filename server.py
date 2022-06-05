from PIL import Image
import socket
from termcolor import colored

port = port to listen on
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(colored(f"[*] Listening... on 0.0.0.0 {port}", "blue"))
    conn, addr = s.accept()
    print(colored(f"[*] Connection accepted from: {addr}", "blue"))
    name = 0
    while True:
        try:
            size = int(conn.recv(10).decode('utf-8'))
            data = conn.recv(size)
        except ValueError:
            print(colored("Value Error...\nClosing...", "red"))
            s.close()
            break
        try:
            img_to_save = Image.frombytes("RGB", (1920, 1080), data)
            name += 1
            img_to_save.save(f"{name}.png")
            print(colored(f"{data}", "white"))
            print(colored(f"[*] Received {name}.png", "blue"))

        except:
            print(colored("\n[-]Closing...", "red"))
            break
main()
