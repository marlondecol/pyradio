from abc import ABC, abstractmethod

from socket import socket

from typing import List

from modules.socket.error import SocketError

from modules.utils.utils import clear


class Node(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """
        Creates a socket instance.
        """

        # Socket object.
        self.__socket = None

        # Event log list.
        self.__logs = None

    def check_connection(self) -> None:
        """
        Checks whether the socket is already open.

        ---
        Raises
        ---

            SocketError
        The socket is closed or undefined.
        """

        # If the socket is not open,...
        if not self.is_open():

            # ... raises an error.
            raise SocketError()

    @abstractmethod
    def disconnect(self) -> None:
        """
        Closes this socket connection.
        """

    def get_logs(self) -> List[str]:
        """
        Allows the child class to get the log list attribute.

        ---
        Returns
        ---

            List(str)
        The log list of this socket.
        """

        # Returns the log list attribute.
        return self.__logs

    def get_socket(self) -> socket:
        """
        Allows the child class to get the socket attribute.

        ---
        Returns
        ---

            socket
        The socket of this socket.
        """

        # Returns the socket attribute.
        return self.__socket

    def is_open(self) -> bool:
        """
        Checks whether the socket is already open.

        ---
        Returns
        ---

            bool
        True for open, False for closed.
        """

        # The socket is closed when the attribute is None.
        return self.__socket is not None

    def log(self, message: str = None) -> None:
        """
        Appends a message to the event log list and print them all again.

        ---
        Arguments
        ---

            message (str, None)
        A message for a event to log.
        """

        # Checks whether the socket is already open.
        self.check_connection()

        # If a message was provided,...
        if message is not None:

            # ... appends it to the event log list.
            self.__logs.append(message)

        # Clears screen before printing the list.
        clear()

        # Prints all of the event messages.
        for line in self.__logs:
            print(line, end='')

    def set_logs(self, logs: List[str]) -> None:
        """
        Allows the child class to set the log list attribute.

        ---
        Arguments
        ---

            logs (List(str))
        The log list to be defined as the log list attribute.
        """

        # Sets the log list attribute.
        self.__logs = logs

    def set_socket(self, sock: socket) -> None:
        """
        Allows the child class to set the socket attribute.

        ---
        Arguments
        ---

            sock (socket)
        The socket to be defined as the socket attribute.
        """

        # Sets the socket attribute.
        self.__socket = sock
