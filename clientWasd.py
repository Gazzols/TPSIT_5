import socket
from pynput import keyboard

IP_SERVER = "192.168.1.126"
PORTA_SERVER = 10000
BUFFER = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_SERVER, PORTA_SERVER))
print("Connesso al server")
print("Usa W A S D per muovere il robot – ESC per uscire")

def on_press(key):
    try:
        if key.char in ["w", "a", "s", "d"]:
            s.send(key.char.encode())
            risposta = s.recv(BUFFER).decode()
            print(f"→ {key.char.upper()} | risposta: {risposta}")
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        print("Chiusura client")
        s.send("s".encode())  # stop di sicurezza
        s.close()
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()