import socket
from AlphaBot import AlphaBot
import RPi.GPIO as GPIO

IP_SERVER = "0.0.0.0"
PORTA_SERVER = 10000
BUFFER = 4096

DR = 16
DL = 19

def main():
    a = AlphaBot()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DR, GPIO.IN)
    GPIO.setup(DL, GPIO.IN)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP_SERVER, PORTA_SERVER))
    s.listen(10)
    print("connesso")

    conn, _ = s.accept()

    while True:
        comando = conn.recv(BUFFER).decode().strip()
        print(f"Comando ricevuto: {comando}")

        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)

        if DR_status == 0 or DL_status == 0:
            print("ostacolo")
            a.stop()
            conn.send("ostacolo".encode())
            continue   # evita di eseguire altri comandi

        if comando == "a":
            a.forword()
            conn.send("ok".encode())
        elif comando == "i":
            a.backward()
            conn.send("ok".encode())
        elif comando == "l":
            a.left()
            conn.send("ok".encode())
        elif comando == "d":
            a.right()
            conn.send("ok".encode())
        elif comando == "s":
            a.stop()
            conn.send("ok".encode())
            break

    conn.close()
    s.close()

if __name__ == "__main__":
    main()