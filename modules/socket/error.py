from socket import socket

from typing import Any


class SocketError(Exception):
    """
    Some fundamental socket error.
    """


class ClientDisconnectedError(SocketError):
    """
    Client disconnected error
    """


class ConnectionTimeoutError(SocketError):
    """
    Connection attempt timed out.
    """


class InvalidClientError(SocketError):
    def __init__(self, sock: socket, client: socket) -> None:
        """
        Client not present in the server client list.

        ---
        Arguments
        ---

            sock (socket)
        The server socket.

            client (socket)
        The client socket of the attempt.
        """

        self.socket = sock
        self.client = client

        super().__init__()


class InvalidNameError(SocketError):
    def __init__(self, sock: socket) -> None:
        """
        Empty client name.

        ---
        Arguments
        ---

            sock (socket)
        The client socket.
        """

        self.socket = sock

        super().__init__()


class InvalidPortError(SocketError):
    def __init__(self, port: Any) -> None:
        """
        Invalid port number for a socket.

        ---
        Arguments
        ---

            port (Any)
        The port of the attempt.
        """

        self.port = port

        super().__init__()


class PortAlreadyUsedError(SocketError):
    def __init__(self, sock: socket, port: Any) -> None:
        """
        Port number already in use.

        ---
        Arguments
        ---

            sock (socket)
        The server socket.

            port (Any)
        The port of the attempt.
        """

        self.socket = sock
        self.port = port

        super().__init__()


class PortOutOfRangeError(SocketError):
    def __init__(self, port: Any) -> None:
        """
        Port number out of range.

        ---
        Arguments
        ---

            port (Any)
        The port of the attempt.
        """

        self.port = port

        super().__init__()


class UndefinedNameError(SocketError):
    """
    Undefined client name.
    """


class UnknownHostError(SocketError):
    def __init__(self, sock: socket, hostname: Any, port: Any) -> None:
        """
        Unknown host to connect.

        ---
        Arguments
        ---

            sock (socket)
        The client socket.

            hostname (Any)
        The hostname of the attempt.

            port (Any)
        The port number of the attempt.
        """

        self.socket = sock
        self.hostname = hostname
        self.port = port

        super().__init__()
