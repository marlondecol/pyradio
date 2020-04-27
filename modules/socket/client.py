from socket import gaierror, socket, timeout

from typing import Optional

from modules.modulator.error import InvalidModulationTypeError

from modules.modulator.modulator import Modulator

from modules.socket.error import (ConnectionTimeoutError, InvalidNameError,
                                  InvalidPortError, UndefinedNameError,
                                  UnknownHostError)

from modules.socket.node import Node

from modules.socket.settings import (ATTEMPT_TIME, DEFAULT_HOST, DEFAULT_PORT,
                                     ENCODING, PACKAGE_SIZE)


class Client(Node):
    def __init__(self, name: str = None) -> None:
        """
        Creates a socket client instance.

        ---
        Arguments
        ---

            name (str, None):
        A name for this client.
        """

        # Gives the name to this client.
        self.set_name(name)

        # Calls the parent init method.
        super().__init__()

    def __str__(self) -> str:
        """
        Called when printing this instance.

        ---
        Returns
        ---

            str
        The name of this client.
        """

        # Returns this client name.
        return self.get_name()

    def check_name(self) -> None:
        """
        Checks whether this client has a name.

        ---
        Raises
        ---

            UndefinedNameError
        The client name is not defined.
        """

        # If the client does not have a name,...
        if self.__name is None:

            # ... raises an error.
            raise UndefinedNameError()

    def connect(self,
                modulation: str,
                hostname: str = DEFAULT_HOST,
                port: int = DEFAULT_PORT) -> None:
        """
        Establishes a connection with a socket server.

        ---
        Arguments
        ---

            modulation (str)
        A modulation type for the audio that this client will receive.

            hostname (str, DEFAULT_HOST)
        A hostname of a server to connect to.

            port (int, DEFAULT_PORT)
        A port number of a server to connect to.

        ---
        Raises
        ---

            InvalidModulationTypeError
        The modulation type is invalid.

            ConnectionRefusedError
        The connection with the server was refused.

            UnknownHostError
        The connection host is unknown or nonexistent.

            KeyboardInterrupt
        If Ctrl+C was pressed.

            InvalidPortError
        The chosen port is not valid.
        """

        # Checks whether this client has a name.
        self.check_name()

        # If the modulation type is not among those available,...
        if modulation not in Modulator.modulations:

            # raises an error.
            raise InvalidModulationTypeError(modulation)

        # If the hostname is empty,...
        if not hostname:

            # ... uses the default one.
            hostname = DEFAULT_HOST

        # If the port is empty,...
        if not port:

            # ... uses the default one.
            port = DEFAULT_PORT

        try:

            # Ensures that the port is an integer.
            port = int(port)

            # Assings the address to a variable.
            server = (hostname, port)

            # Instantiates a socket object with the default settings.
            sock = socket()

            # Sets the connection attempt timeout.
            sock.settimeout(ATTEMPT_TIME)

            # Tries to connect.
            sock.connect(server)

        # Connection with the server was refused.
        except ConnectionRefusedError:
            raise ConnectionRefusedError()

        # Ctrl+C pressed.
        except (EOFError, KeyboardInterrupt):
            raise KeyboardInterrupt()

        # Unknown or nonexistent host.
        except gaierror:
            raise UnknownHostError(sock, hostname, port)

        # Connection timeout.
        except timeout:
            raise ConnectionTimeoutError()

        # Port is not valid.
        except ValueError:
            raise InvalidPortError(port)

        # Resets the socket timeout setting.
        sock.settimeout(None)

        # The client socket address.
        self.__address = sock.getsockname()

        # Event log list.
        self.set_logs([])

        # Chosen modulation type.
        self.__modulation = modulation

        # Server address.
        self.__server = server

        # The client socket.
        self.set_socket(sock)

        # Sends the client name automatically.
        self.send_str(self.__name)

        # Receives the log accent color.
        self.__color = self.recv_str()

        # Sends the modulation type automatically.
        self.send_str(self.__modulation)

    def disconnect(self) -> None:
        """
        Closes this client socket connection.
        """

        # Checks whether the socket is already open.
        if self.is_open():

            # Closes the socket.
            self.get_socket().close()

        # Reset the client socket address.
        self.__address = None

        # Reset the events logs.
        self.set_logs(None)

        # Reset the modulation type.
        self.__modulation = None

        # Reset the server address.
        self.__server = None

        # Reset the socket.
        self.set_socket(None)

    def get_name(self) -> str:
        """
        Allows to get the client name.

        ---
        Returns
        ---

            str
        The client name.
        """

        # Returns the client name.
        return self.__name

    def recv(self) -> bytes:
        """
        Receives a package from the server.

        ---
        Returns
        ---

            bytes
        The received package.
        """

        # Checks whether the socket is already open.
        self.check_connection()

        # Returns the received package.
        return self.get_socket().recv(PACKAGE_SIZE)

    def recv_str(self) -> str:
        """
        Receives a string from the server.

        ---
        Returns
        ---

            str
        The received string.
        """

        # Returns the received string.
        return self.recv().decode(ENCODING)

    def send(self, package: bytes, ensure: bool = True) -> Optional[int]:
        """
        Sends a package to the server.

        ---
        Arguments
        ---

            package (bytes)
        A package to send.

            ensure (bool, True)
        Sets whether the package should be guaranteed delivery.

        ---
        Returns
        ---

            Optional(int)
        Number of bytes sent, if ensure flag is True.
        """

        # Checks whether the socket is already open.
        self.check_connection()

        # Sends the package to the server, with or without delivery guarantee.
        return self.get_socket().send(
            package) if ensure else self.get_socket().sendall(package)

    def send_str(self, string: str, ensure: bool = True) -> Optional[int]:
        """
        Sends a string to the server.

        ---
        Arguments
        ---

            string (str)
        A strign to send.

            ensure (bool, True)
        Sets whether the string should be guaranteed delivery.

        ---
        Returns
        ---

            Optional(int)
        Number of bytes sent, if ensure flag is True.
        """

        # Sends the encoded string to the server, with or without delivery
        # guarantee.
        return self.send(string.encode(ENCODING), ensure)

    def set_name(self, name: str = None) -> None:
        """
        Sets the client name.

        ---
        Arguments
        ---

            name (str, None)
        A name to set to this client.

        ---
        Raises
        ---

            InvalidNameError
        The provided name is empty.
        """

        # If a name was provided,...
        if name is not None:

            # ... and is empty,...
            if not name:

                # ...raises an error.
                raise InvalidNameError(self.get_socket())

            # If no, convert it to a string.
            name = str(name)

        # Attributes the name.
        self.__name = name
