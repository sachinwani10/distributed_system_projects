"""
Name: Sachin Ravindra Wani
Student ID: 1001563321
"""
import socket
import os
from threading import Thread


class Client:
    """
    Driver functionality
    """
    def __init__(self, name, user_input):

        self.name = name
        self.user_input = user_input
        self.result = 0
        self.initial = 1
        self.logname = self.name + "_log" + ".txt"
        self.f = open(self.logname, "w")

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
                # msg = 'sachin'
                # self.s.send(msg.encode())
                serverPollHandler = PollHandler(self)
                serverPollHandler.start()
                print("Enter The operations: ")
            elif user_choice == 'n':
                msg = 'stop'
                self.s.send(msg.encode())
                self.s.close()
                exit(1)
            else:
                operation = user_choice
                if user_choice != 'n':
                    print("Initial value: " + str(self.initial))
                    self.f = open(self.logname, "a")
                    self.f.write(operation + "\n")
                    self.f.close()
                    self.calculator(operation)
                    print(operation)
                    print("Initial Changed to: " + str(self.result))

        except RuntimeError:
            print("Error")


class PollHandler(Thread):

    def __init__(self, client):
        Thread.__init__(self)
        self.name = client.name
        self.f = client.f
        self.s = client.s
        self.logname = self.name + "_log" + ".txt"
        self.client = client

    def run(self):
        while True:
            data = self.s.recv(1024).decode()
            if data:
                print(data)

            if os.path.exists(self.logname):
                # Send number of lines in log to the server
                self.f = open(self.logname, "r")
                count = len(self.f.readlines())
                self.s.send(str(count).encode())
                self.f.close()

                # server will send how many lines it received
                data = str(self.s.recv(1024).decode())
                print(data)

                # Send all the operations to the server in string
                self.f = open(self.logname, "r")
                data = self.f.readlines()
                str1 = ''.join(data)
                self.f.close()
                print(str1)
                self.s.send(str1.encode())

                # clear the log after all operations are sent to server
                os.remove(self.logname)

                # Receive new Initial from server
                data = str(self.s.recv(1024).decode())
                self.client.initial = int(data)

                # notifying on gui abt changed value of Initial
                print("Initial value changed to: " + str(self.client.initial))
            else:
                msg = "log is empty"
                self.s.send(msg.encode())
