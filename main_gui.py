"""
Name: Sachin Ravindra Wani
Student ID: 1001563321
"""

import sys
import tkinter as tk
from threading import Thread
# from ds_server import run_server, get_client_list
from ds_server import ServerHandler
import subprocess as sub
# from child_gui import run_client_ui


class MainWindow(tk.Tk):
    """
    Main GUI Window
    """
    def __init__(self):
        self.srvr = ServerHandler()
        tk.Tk.__init__(self)
        self.geometry('500x250')
        self.title('Server')
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        b1 = tk.Button(self, text="start Server", command=self.start_server)
        b1.pack(in_=toolbar, side="left")
        b2 = tk.Button(self, text="start client", command=self.start_client)
        b2.pack(in_=toolbar, side="left")
        b3 = tk.Button(self, text="Stop Server", command=self.stop_server)
        b3.pack(in_=toolbar, side="left")
        b4 = tk.Button(self, text="Active Clients", command=self.srvr.get_client_list)
        b4.pack(in_=toolbar, side="left")
        b5 = tk.Button(self, text="Poll Clients", command=self.srvr.poll_client)
        b5.pack(in_=toolbar, side="left")
        text = tk.Text(self, wrap="word", yscrollcommand=scrollbar.set)
        text.pack(side="top", fill="both", expand=True)
        text.see("end")
        scrollbar.config(command=text.yview)
        self.server = None
        self.processes = []

        # redirect stdout to tkinter Text widget
        try:
            # sys.stdout = TextRedirector(text, self.processes, tag="stdout")
            sys.stdout.write = decorator(sys.stdout.write, text)
        except:
            print("App Closed")

    def start_server(self):
        """
        starts Server on new thread
        :return: None
        """
        self.server = Thread(target=self.srvr.run_server)
        self.server.start()

    def start_client(self):
        """
        Starts client as new process(note that it is not a thread )
        :return: None
        """
        p = sub.Popen(['python', 'child_gui.py'])
        self.processes.append(p)

    def stop_server(self):
        """
        Stop server thread and close the GUI
        :return:
        """
        # tk.Tk.quit(self)
        tk.Tk.destroy(self)
        self.server.join(0.1)
        sys.exit(0)


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


# class TextRedirector(object):
#     """
#     All print statement output(stdout) will be redirected to tkinter Text widget
#     """
#     def __init__(self, widget, processes, tag="stdout"):
#         self.widget = widget
#         self.tag = tag
#         self.processes = processes
#
#     def write(self, str):
#         try:
#             self.widget.configure(state="normal")
#             self.widget.insert("end", str, (self.tag,))
#             self.widget.configure(state="disabled")
#         except:
#             print("App closed")
#             for p in self.processes:
#                 p.kill()


app = MainWindow()
app.mainloop()

