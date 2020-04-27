from threading import Thread

from modules.core.options import connect, set_name

from modules.core.threads import handle_client

from modules.formatter.colors import GREEN

from modules.formatter.formatter import Formatter as F

from modules.socket.client import Client

from modules.socket.error import (InvalidPortError, PortAlreadyUsedError,
                                  PortOutOfRangeError)

from modules.socket.server import Server

from modules.socket.settings import DEFAULT_PORT

from modules.utils.utils import (_l, _lt, _ltb, ellipsis, error, label,
                                 press_enter_to, success, title)


def client_option() -> None:
    """
    "Client" main menu option.
    """

    # Instantiates a brand new client.
    client = Client()

    try:

        # Waits for the user to provide the client name.
        set_name(client, F().blue())

        while True:
            print(F().magenta(title()))
            print(
                _l(F().magenta('Welcome, {}!'.format(F().bold(
                    client.get_name())))))
            print(_ltb('What do you want to do?'))

            # Sets the client menu options, with their respective methods.
            options = [['Connect to a server', 'connect'],
                       ['Change my name', 'set_name']]

            # Lists the options.
            for i, option in enumerate(options):
                print(_l(label(option[0], F().red(i + 1), F())))

            print(_l(label('Quit to main menu', F().red(0), F())))

            # Reads the chosen option.
            try:
                opt = int(input(_lt('Your option: ')))

                # Checks whether the option is available.
                if opt not in range(0, len(options) + 1):
                    raise ValueError()

            # Invalid or nonexisting option.
            except ValueError:
                print(_lt(error('Invalid option!')))
                press_enter_to('try again', F().red(), F().white())

                continue

            # If the option is 0, quit to main menu.
            if not opt:
                break

            try:

                # If no, runs the corresponding function.
                globals()[options[opt - 1][1]](client)

            # Ctrl+C pressed.
            except (EOFError, KeyboardInterrupt):
                pass

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        pass

    del client


def server_option() -> None:
    """
    "Server" main menu option.
    """

    # Instantiates a brand new server.
    server = Server(GREEN)

    try:
        while True:
            print(F().blue(title()))
            print(_l(F().blue('Configure the connection for this server.')))

            try:

                # Waits for the user to provide the server port number.
                port = input(
                    _lt('Port number [{}]: '.format(
                        F().bold().magenta(DEFAULT_PORT))))

                print()

                # Sets the feedback animation thread...
                thread = Thread(target=ellipsis,
                                args=(_l('Starting'), F().yellow()),
                                daemon=True)

                # ... and starts it.
                thread.start()

                try:

                    # Binds the port number to the server and tries to connect.
                    server.connect(port=port)

                # Ctrl+C pressed.
                except (EOFError, KeyboardInterrupt):

                    # Stops the feedback animation thread.
                    thread.alive = False

                    print(_lt(_lt(error('Operation canceled by the user!'))))
                    press_enter_to('try again', F().red(), F().white())

                    continue

                # Stops the feedback animation thread when the connection is established.
                thread.alive = False

                print(_lt(_lt(success('Server started successfully!'))))
                press_enter_to('continue', F().green(), F().white())

                break

            # Port is not valid.
            except InvalidPortError:
                err = 'The provided port number is invalid!'

            # Port is already in use.
            except PortAlreadyUsedError as _e:
                err = 'The port number {:d} is already in use!'.format(_e.port)

            # Port number out of range.
            except PortOutOfRangeError:
                err = 'The port number must be between 0 and 65535!'

            # Stops the feedback animation thread.
            thread.alive = False

            print(_lt(_lt(error(err))))
            press_enter_to('try again', F().red(), F().white())

        server.log(F().green(title(clear_screen=False)))

        # Gets the connection address.
        host, port = server.address()

        # Shows the address in the log.
        server.log(
            _lt(
                label(F().bold().green(
                    'Connection established at {}:{}!'.format(host, port)))))

        # Info message.
        server.log(_lt(label(F().cyan('Recording audio through microphone'))))
        server.log(_lt(label(F().bold().blue('Press Ctrl+C to shutdown'))))

        try:

            # Runs this until Ctrl+C is pressed.
            while True:

                # Accepts a new client.
                client = server.hello()

                # Starts the thread that handles this client.
                Thread(target=handle_client,
                       args=(
                           server,
                           client,
                       ),
                       daemon=True).start()

        # Ctrl+C pressed.
        except (EOFError, KeyboardInterrupt):
            server.log(_ltb(label(error('Closing connection...'))))

            # Shutdowns the server.
            server.disconnect()

            press_enter_to('back to main menu', F().red(), F().white())

    # Ctrl+C pressed.
    except (EOFError, KeyboardInterrupt):
        pass

    # Shutdowns the server.
    server.disconnect()

    del server
