from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import csv

class chat:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.connect_to_server()

        self.top = tkinter.Tk()
        self.top.title("Chat")
        self.top.geometry("+0+0")

        self.messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()
        self.my_msg.set("")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)
        self.msg_list = tkinter.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT)
        self.messages_frame.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.top, text="Envoyer", command=self.send)
        self.send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

        self.load_chat_from_csv()

        tkinter.mainloop()

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.ADDR)
        except ConnectionRefusedError:
            print("Erreur de connexion: le serveur de chat n'est pas accessible.")
            exit(1)

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tkinter.END, msg)
                self.save_chat_to_csv()
            except OSError:
                break

    def send(self, event=None):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.top.quit()

    def on_closing(self, event=None):
        self.my_msg.set("{quit}")
        self.send()

    def save_chat_to_csv(self):
        with open('Chat.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.msg_list.get(0, tkinter.END))

    def load_chat_from_csv(self):
        try:
            with open('Chat.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for message in reader:
                    self.msg_list.insert(tkinter.END, message[0])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    HOST = 'localhost'  # Utilisation de 'localhost' comme adresse IP par défaut
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    chat = chat(HOST, PORT)