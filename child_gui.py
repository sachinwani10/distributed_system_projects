"""
Name: Sachin Ravindra Wani
Student ID: 1001563321
"""

from ds_client import Client
import tkinter as tk
import sys
from ds_client import ManageLog


class MainWindow(tk.Tk):
    """
    client GUI window
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('550x250')
        self.title('Client')
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        # b1 = tk.Button(self, text="Clear Log", command=self.clear_log)
        # b1.pack(in_=toolbar, side="left")
        # b3 = tk.Button(self, text="Print Log", command=self.print_log)
        # b3.pack(in_=toolbar, side="left")
        self.user_input = tk.StringVar()

        self.b2 = tk.Button(self, text="Send", command=self.start_client)
        self.b2.pack(in_=toolbar, side="right")
        entry_box = tk.Entry(textvariable=self.user_input)
        entry_box.pack(in_=toolbar, side="right")

        text = tk.Text(self, wrap="word", yscrollcommand=scrollbar.set)
        text.insert(tk.END, "Enter Username to connect")
        text.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        try:
            sys.stdout.write = decorator(sys.stdout.write, text)
        except:
            print("App Closed")

    def start_client(self):
        """
        Connects the client to the server
        :return: None
        """
        try:
            name = self.user_input.get()
            global client
            client = Client(name, self.user_input)
            self.b2.configure(command=client.send_message)
            print("Do you wish to continue? y/n")
        except RuntimeError:
            print("Error")

    def clear_log(self):
        logger = ManageLog()
        logger.clear_log()

    def print_log(self):
        logger = ManageLog()
        logger.print_log()


def decorator(func, widget):
    def inner(inputStr):
        try:
            widget.configure(state="normal")
            widget.insert("end", inputStr, ("stdout",))
            widget.configure(state="disabled")
            return func(inputStr)
        except:
            return func(inputStr)
    return inner


def run_client_ui():
    app = MainWindow()
    app.mainloop()


run_client_ui()
