from itertools import cycle

from select import select

from socket import socket

from typing import List, Optional, Tuple

from modules.formatter.formatter import Formatter as F

from modules.socket.error import (ClientDisconnectedError, InvalidClientError,
                                  InvalidPortError, PortAlreadyUsedError,
                                  PortOutOfRangeError)

from modules.socket.node import Node

from modules.socket.settings import (BACKLOG_SIZE, COLORS, DEFAULT_PORT,
                                     ENCODING, PACKAGE_SIZE)


class Server(Node):
    def __init__(self, color: str) -> None:
        """
        Creates a socket server instance.

        ---
        Arguments
        ---

            color (str)
        A Formatter's color constant.
        """

        # Check whether the color is valid.
        F().check_color(color)

        # Server log accent color.
        self.__color = color

        # Available log accent colors for the incoming clients.
        self.__client_colors = cycle(COLORS)

        # Calls the parent init method.
        super().__init__()

    def address(self, client: socket = None) -> Tuple[str, int]:
        """
        Gets both host and port from this server or from one of its clients.

        ---
        Arguments
        ---

            client (socket, None)
        A client socket object from which the address will be obtained, if not
        from the server.

        ---
        Returns
        ---

            Tuple(str, int)
        Both the host and the port, respectively.
        """

        # If the client socket was not provided,...
        if client is None:

            # ... checks whether the socket is already open...
            self.check_connection()

            # ... and returns the socket address of this server.
            return self.get_socket().getsockname()

        # Checks the client connection.
        self.check_client(client)

        # Returns the client address.
        return client.getpeername()

    def broadcast(self,
                  package: bytes,
                  black_list: List[socket] = None,
                  ensure: bool = True) -> None:
        """
        Sends a package to all of this server clients. A blacklist can be
        provided with clients which the package should not be sent.

        ---
        Arguments
        ---

            package (bytes)
        A package to send.

            black_list (List(socket), None)
        A list of clients which the package should not be sent.

            ensure (bool, True)
        Sets whether the package should be guaranteed delivery.
        """

        # If `black_list` was not provided,...
        if black_list is None:

            # ... then assigns it an empty list.
            black_list = []

        # Checks whether the socket is already open.
        self.check_connection()

        # For each connected client,...
        for client in list(set(self.__clients) - set(black_list)):

            # ... sends the package.
            self.send(client, package, ensure)

    def broadcast_str(self,
                      string: str,
                      black_list: List[socket] = None,
                      ensure: bool = True) -> None:
        """
        Sends a string to all of this server clients. A blacklist can be
        provided with clients which the string should not be sent.

        ---
        Arguments
        ---

            string (str)
        A string to send.

            black_list (List(socket), None)
        A list of clients which the string should not be sent.

            ensure (bool, True)
        Sets whether the string should be guaranteed delivery.
        """

        # Sends the encoded string to all of the connected clients, except for
        # those among the black list.
        self.broadcast(string.encode(ENCODING), black_list, ensure)

    def bye(self, client: socket) -> None:
        """
        Disconnects a client from this server.

        ---
        Arguments
        ---

            client (socket)
        A client socket to disconnect.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        # Close the client socket.
        client.close()

        # Removes the client from the server client list.
        del self.__clients[client]

    def check_client(self, client: socket) -> None:
        """
        Checks whether a client is connected to this server.

        ---
        Arguments
        ---

            client (socket)
        A client socket from which the connection will be checked.

        ---
        Raises
        ---

            InvalidClientError
        The client is not connected to this server.
        """

        # Checks whether the socket is already open.
        self.check_connection()

        # If the client is not present in the server client list,...
        if client not in self.__clients.keys():

            # ... raises an error.
            raise InvalidClientError(self.get_socket(), client)

    def connect(self, host: str = '', port: int = DEFAULT_PORT) -> None:
        """
        Opens a socket connection to this server.

        ---
        Arguments
        ---

            host (str, '')
        A hostname to bind to this server.

            port (int, DEFAULT_PORT)
        A port number to bind to this server.

        ---
        Raises
        ---

            PortAlreadyUsedError
        The chosen port is already in use.

            InvalidPortError
        The chosen port is not valid.
        """

        # If the port is empty,...
        if not port:

            # ... uses the default one.
            port = DEFAULT_PORT

        try:

            # Ensures that the port is an integer.
            port = int(port)

            # Instantiates a socket object with the default settings.
            sock = socket()

            # Binds the host and the port to the socket.
            sock.bind((host, port))

        # Port is already in use.
        except OSError:
            raise PortAlreadyUsedError(sock, port)

        # Port number out of the valid range.
        except OverflowError:
            raise PortOutOfRangeError(port)

        # Port is not valid.
        except ValueError:
            raise InvalidPortError(port)

        # Connected clients.
        self.__clients = {}

        # Event log list.
        self.set_logs([])

        # Connection port.
        self.__port = port

        # The server socket.
        self.set_socket(sock)

        # Wait for new connections.
        self.get_socket().listen(BACKLOG_SIZE)

    def disconnect(self) -> None:
        """
        Closes this server socket connection.
        """

        # Checks whether the socket is already open.
        if self.is_open():

            # For each connected client,...
            for client in self.__clients:

                # ... and closes the connection.
                client.close()

            # Closes the socket.
            self.get_socket().close()

        # Reset the client list.
        self.__clients = None

        # Reset the events logs.
        self.set_logs(None)

        # Reset the socket.
        self.set_socket(None)

    def get_color(self, client: socket) -> str:
        """
        Gets the color from a connected client.

        ---
        Arguments
        ---

            client (socket)
        A client socket from which the color will be obtained.

        ---
        Returns
        ---

            str
        The client Formatter's color.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        # Return the Formatter color string assigned to the client.
        return self.__clients[client]['color']

    def get_modulation(self, client: socket) -> str:
        """
        Gets the modulation type from a connected client.

        ---
        Arguments
        ---

            client (socket)
        A client socket from which the modulation type will be obtained.

        ---
        Returns
        ---

            str
        The client modulation type string.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        # Returns the modulation type string.
        return self.__clients[client]['modulation']

    def get_name(self, client: socket) -> str:
        """
        Gets the name of a connected client.

        ---
        Arguments
        ---

            client (socket)
        A client socket from which the name will be obtained.

        ---
        Returns
        ---

            str
        The client name.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        # Returns the name string.
        return self.__clients[client]['name']

    def hello(self) -> socket:
        """
        Accepts a new client connection.

        ---
        Returns
        ---

            socket
        The socket object of the brand new client.
        """

        # Checks whether the socket is already open.
        self.check_connection()

        # While the socket is still open,...
        while self.is_open():

            # ... checks if there is some response from the socket.
            response, _, _ = select([self.get_socket()], [], [], 0.1)

            # While the socket is responding,...
            if response:

                # ... accepts a client that is attempting to connect.
                client, _address = self.get_socket().accept()

                break

        # Selects the next color.
        color = next(self.__client_colors)

        # Creates a new client, setting his log accent color.
        self.__clients[client] = {'color': color}

        # Receives and sets his name.
        self.__clients[client]['name'] = self.recv_str(client)

        # Sends him back the defined color.
        self.send_str(client, color)

        # Receives and sets his chosen modulation type.
        self.__clients[client]['modulation'] = self.recv_str(client)

        # Returns the client socket object.
        return client

    def recv(self, client: socket) -> bytes:
        """
        Receives a package from a client.

        ---
        Arguments:
        ---

            client (socket)
        A client socket from which the package will be received.

        ---
        Returns:
        ---

            bytes
        The received package.
        """

        # Returns the received package.
        return client.recv(PACKAGE_SIZE)

    def recv_str(self, client: socket) -> str:
        """
        Receives a string from a client.

        ---
        Arguments
        ---

            client (socket)
        A client socekt from which the string will be received.

        ---
        Returns
        ---

            str
        The received string.
        """

        # Returns the received string.
        return self.recv(client).decode(ENCODING)

    def send(self,
             client: socket,
             package: bytes,
             ensure: bool = True) -> Optional[int]:
        """
        Sends a package to a client.

        ---
        Arguments
        ---

            client (socket)
        A client socket to which the package will be sent.

            package (bytes)
        A package to send.

            ensure (bool, True)
        Sets whether the package should be guaranteed delivery.

        ---
        Raises
        ---

            ClientDisconnectedError
        Not connected client.

        ---
        Returns
        ---

            Optional(int)
        Number of bytes sent, if ensure flag is True.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        try:

            # Sends the package to the client, with or without delivery guarantee.
            return client.send(package) if ensure else client.sendall(package)

        # If the client disconnected,...
        except (BrokenPipeError, ConnectionResetError, OSError):

            # ... raises an error.
            raise ClientDisconnectedError()

    def send_str(self,
                 client: socket,
                 string: str,
                 ensure: bool = True) -> Optional[int]:
        """
        Sends a string to a client.

        ---
        Arguments
        ---

            client (socket)
        A client socket to which the string will be sent.

            string (str)
        A string to send.

            ensure (bool, True)
        Sets whether the string should be guaranteed delivery.

        ---
        Returns
        ---

            Optional(int)
        Number of bytes send, if ensure flag is True.
        """

        # Checks whether the client is connected to this server.
        self.check_client(client)

        # Sends the encoded string to the client, with or without delivery
        # guarantee.
        return self.send(client, string.encode(ENCODING), ensure)
