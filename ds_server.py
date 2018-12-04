"""
Name: Sachin Ravindra Wani
Student ID: 1001563321
"""
import socket
from threading import Thread

threads = []  # this list store all active client threads


class ClientThread(Thread):
    def __init__(self, host, port, conn, address, thread_list):
        """
        Creates an instance of Server handler for client
        :param host: hostname of machine
        :type host: int
        :param port: Socket port number
        :type port: int
        :param conn: handles connection with client
        :type conn: object
        :param address: address of the client
        :type address: list
        :param threads: stores all active client threads
        :type threads: list
        """
        Thread.__init__(self)
        self.ip = host
        self.port = port
        self.conn = conn
        self.addr = address
        self.threads = thread_list
        self.name = ""
        # self.result = 0
        # self.initial = 1
        print("Connection has been established with " + self.name + " |" + "IP " + address[0] + " | Port " + str(port))

    def stop(self):
        """
        remove any thread which is no longer active
        :return: None
        """
        self.threads.remove(self)

    def get_client_name(self):
        return self.name

    def run(self):
        """
        All the interaction with client thread is handled here
        :return: None
        """
        message = "Enter your Username: "
        self.conn.send(message.encode())
        data = str(self.conn.recv(1024).decode())
        message = data + ' Registered Successfully \n'
        self.name = data
        print("notified client " + data + " of Successful Registration \n")
        self.conn.send(message.encode())

        disconnection = ClientDisconnectionHandler(self)
        disconnection.start()


    def server_calculator(self, user_operation, initial):
        base_value = initial
        number = int(user_operation.split(' ')[1])
        operation = user_operation.split(' ')[0]
        try:
            if operation == '+':
                result = base_value + number
                base_value = result

            if operation == '-':
                result = base_value - number
                base_value = result

            if operation == '*':
                result = base_value * number
                base_value = result

            if operation == '/':
                try:
                    result = base_value / number
                    base_value = result
                except ZeroDivisionError as err:
                    print(err)
        except Exception as err:
            print(err)
            exit(1)
        return base_value

    def receive_operations(self, initial):
        # After receiving this message client will stop waiting and will send the operations to be performed on the
        # Initial value
        base_value = initial
        msg = "Server polled Client " + self.name
        print(msg)
        self.conn.send(msg.encode())

        # receive number of operations
        data = str(self.conn.recv(1024).decode())
        if data == 'log is empty':
            print("Log is empty for client: " + self.name)
            return 1

        number_of_operations = int(data)
        msg = "Server Received " + str(number_of_operations) + " operations from Client " + self.name
        print(msg)
        self.conn.send(msg.encode())

        # receive actual operations from the client
        data = str(self.conn.recv(1024).decode())
        operation_list = data.split("\n")

        # perform the operations on initial value
        for operation in operation_list:
            if operation:
                base_value = self.server_calculator(operation, base_value)
        # print("this is result after all operations from client: " + str(result))
        return base_value


class ServerHandler:
    def __init__(self):
        self.result = 0
        self.initial = 1

    def run_server(self):
        """
        driver function
        :return:None
        """
        # Create Socket
        try:
            host = ''
            port = 5000
            s = socket.socket()
        except socket.error as msg:
            print("Socket Creation error: " + str(msg))

        # Bind socket to the port
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(3)
        # listen and accept incoming connections
        while True:
            try:
                print("Listening...\n")
                conn, address = s.accept()
                # create new thread for every new client connection
                try:
                    newThread = ClientThread(host, port, conn, address, threads)
                    newThread.start()

                    threads.append(newThread)
                except RuntimeError as err:
                    print(err)
                    for t in threads:
                        t.join()
            except OSError as e:
                print(e)
                print("Someone disconnected!")

    def get_client_list(self):
        """
        Prints all active clients
        :return: None
        """
        # for c in threads:
        #     print(c.get_client_name)
        print([c.get_client_name() for c in threads])

    def poll_client(self):
        for c in threads:
            self.result = c.receive_operations(self.initial)
            self.initial = self.result
        print("Final Result: " + str(self.result))
        print("New Initial: " + str(self.result))
        msg = str(self.result)
        for c in threads:
            c.conn.send(msg.encode())


class ClientDisconnectionHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            data = str(self.client.conn.recv(1024).decode())
            if data == 'stop':
                self.client.conn.close()
                print(self.client.name + " disconnected!\n")
                self.client.stop()
                break
            else:
                break

