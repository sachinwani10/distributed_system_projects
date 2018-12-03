"""
Name: Sachin Ravindra Wani
Student ID: 1001563321
"""
import socket
import os
from threading import Thread
# from random import randrange
# from time import sleep


class Client:
    """
    Driver functionality
    """
    def __init__(self, name, user_input):

        self.name = name
        self.user_input = user_input
        self.result = 0
        self.initial = 1
        self.f = open("log.txt", "w")

        try:
            host = '127.0.0.1'
            port = 5000
            # create socket
            self.s = socket.socket()
        except socket.error as msg:
            print("Socket error " + str(msg))

        try:
            # connect to remote server
            self.s.connect((host, port))
            print("Connection Successful!!!")
        except socket.error as msg:
            print("Connection error " + str(msg))

        # Sending username to the server
        data = str(self.s.recv(1024).decode())
        print(data + "\n")
        while True:
            try:
                if self.name:
                    self.s.send(self.name.encode())
                    data = str(self.s.recv(1024).decode())
                    print(data)
                    break
                else:
                    print("Enter Valid User Input")
            except socket.error as msg:
                print(msg)

    def calculator(self, user_operation):
        number = int(user_operation.split(' ')[1])
        operation = user_operation.split(' ')[0]
        try:
            if operation == '+':
                self.result = self.initial + number
                self.initial = self.result

            if operation == '-':
                self.result = self.initial - number
                self.initial = self.result

            if operation == '*':
                self.result = self.initial * number
                self.initial = self.result

            if operation == '/':
                try:
                    self.result = self.initial / number
                    self.initial = self.result
                except ZeroDivisionError as err:
                    print(err)
        except Exception as err:
            print(err)
            exit(1)
        return

    def send_message(self):
        """
        Send random wait time to the server and wait for response
        :return: None
        """
        try:
            user_choice = self.user_input.get()
            if user_choice == 'y':
                serverPollHandler = PollHandler(self.f, self.name, self.s)
                serverPollHandler.start()
                print("Enter The operations: ")
            elif user_choice == 'n':
                msg = 'stop'
                self.s.send(msg.encode())
                # break
            else:
                operation = user_choice
                print("Initial value: " + str(self.initial))
                self.f = open("log.txt", "a")
                self.f.write(operation + "\n")
                self.f.close()
                self.calculator(operation)
                print(operation)
                print("Initial Changed to: " + str(self.result))

        except RuntimeError:
            print("Error")


class ManageLog:
    def clear_log(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")
            print("\nLog Cleared")
        else:
            print("\nLog is empty")


    def print_log(self):
        if os.path.exists("log.txt"):
            f = open("log.txt", "r")
            print("\n-------LOG-------")
            for line in f:
                if(line != ''):
                    print(line)
                else:
                    print("Log Empty\n")
            f.close()
            print("-------END-------")
        else:
            print("\n-------LOG-------")
            print("\nLog is empty\n")
            print("-------END-------")


class PollHandler(Thread):

    def __init__(self, f, name, s):
        Thread.__init__(self)
        self.name = name
        self.f = f
        self.s = s

    def run(self):
        while True:
            data = self.s.recv(1024).decode()
            if data:
                print(data)
                # break
            if os.path.exists("log.txt"):
                # Send number of lines in log to the server
                self.f = open("log.txt", "r")
                count = len(self.f.readlines())
                self.s.send(str(count).encode())
                self.f.close()

                # server will send how many lines it received
                data = str(self.s.recv(1024).decode())
                print(data)

                # Send all the operations to the server in string
                self.f = open("log.txt", "r")
                data = self.f.readlines()
                str1 = ''.join(data)
                self.f.close()
                print(str1)
                self.s.send(str1.encode())

                # clear the log after all operations are sent to server
                os.remove("log.txt")
            else:
                msg = "log is empty"
                self.s.send(msg.encode())
