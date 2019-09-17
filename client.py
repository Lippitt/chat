# on immediate connection, client tells server username
# infinite loop of if client has message to send, send that message and also receive any incoming messages


import socket
import select
import errno
import sys
import tkinter as tk
from tkinter import simpledialog
import time
from threading import Thread

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# action a popup window to prompt user for a username, prevents user being able to change username after being set
def popup():

    popup.my_username = simpledialog.askstring("Create username", "set username")
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    username = popup.my_username.encode("utf-8")
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header + username)


def receive():
    while True:
        try:
            # receive data

            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            # v.set(username + ": " + message)
            msg_list.insert(tk.END, username + ": " + message)

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('read error', str(e))
                sys.exit()

        except Exception as e:
            print('General error', str(e))
            sys.exit()


def send():

    message = textField.get()
    textField.delete(0, tk.END)
    msg_list.insert(tk.END, str(popup.my_username) + ": " + str(message))
    # if message contains data, send it
    message = message.encode("utf-8")
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)


def on_closing():
    client_socket.close()
    root.quit()


root = tk.Tk()
root.title("Chat Client")

popup()

messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

textField = tk.Entry(root)

textField.pack()

beginButton = tk.Button(text="chat", command=send)

beginButton.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)


receive_thread = Thread(target=receive)
receive_thread.start()


root.mainloop()