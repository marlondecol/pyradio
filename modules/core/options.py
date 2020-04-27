from threading import Thread

import numpy as np

import sounddevice as sd

from modules.audio.settings import CHANNELS, CHUNK_SIZE, FRAME_RATE

from modules.formatter.formatter import Formatter as F

from modules.modulator.constants import AM, AM_SC, NO_MOD

from modules.modulator.modulator import Modulator as M

from modules.socket.client import Client

from modules.socket.error import (ConnectionTimeoutError, InvalidNameError,
                                  InvalidPortError, UnknownHostError)

from modules.socket.settings import DEFAULT_HOST, DEFAULT_PORT

from modules.utils.utils import (_l, _lt, _ltb, ellipsis, error, label,
                                 press_enter_to, success, title)


def connect(client: Client) -> None:
    """
    "Connect to a server" client menu option.

    ---
    Arguments
    ---

        client (Client)
    The client instance which wants to connect to a server.
    """

    # Asks the user for the modulation type until it is valid.
    while True:
        print(F().magenta(title()))
        print(_l(F().magenta('Choose a modulation type.\n')))

        # Sets the available modulation types.
        options = [
            [
                '{} - {}'.format(F().bold('AM'),
                                 F().italic('Amplitude Modulation')), AM
            ],
            [
                '{} - {}'.format(
                    F().bold('AM-SC'),
                    F().italic(
                        'Amplitude Modulation with Suppressed Carrier')), AM_SC
            ], [F().italic('No modulation'), NO_MOD]
        ]

        # Lists the options.
        for i, option in enumerate(options):
            print(_l(label(option[0], F().red(i + 1), F())))

        # Reads the chosen option.
        try:
            opt = int(input(_lt('Your option: ')))

            # Checks whether the option is avaliable.
            if opt not in range(1, len(options) + 1):
                raise ValueError()

        # Invalid or nonexisting option.
        except ValueError:
            print(_lt(error('Invalid option!')))
            press_enter_to('try again', F().red(), F().white())

            continue

        # If the option is 0, go back to client menu.
        if not opt:
            break

        # If no, saves the modulation type in a variable.
        modulation = options[opt - 1][1]

        # Goes to the next step.
        break

    # Asks the user for the connection settings until they are valid.
    while True:
        print(F().magenta(title()))
        print(_l(F().magenta('Configure the connection with the server.')))

        try:

            # Waits for the user to provide the hostname.
            host = input(
                _lt('Hostname [{}]: '.format(
                    F().bold().magenta(DEFAULT_HOST))))

            # Waits for the user to provide the port number.
            port = input(
                _l('Port number [{}]: '.format(
                    F().bold().magenta(DEFAULT_PORT))))

            print()

            # Sets the feedback animation thread...
            thread = Thread(target=ellipsis,
                            args=(_l('Connecting'), F().yellow()),
                            daemon=True)

            # ... and starts it.
            thread.start()

            try:

                # Tries to connect with the server.
                client.connect(modulation, host, port)

            # Ctrl+C pressed.
            except (EOFError, KeyboardInterrupt):

                # Stops the feedback animation thread.
                thread.alive = False

                print(_lt(_lt(error('Operation canceled by the user!'))))
                press_enter_to('try again', F().red(), F().white())

                continue

            # Stops the feedback animation thread when the connection is established.
            thread.alive = False

            print(_lt(_lt(success('Connection established!'))))
            press_enter_to('continue', F().green(), F().white())

            # Sends a confirmation of receiving to the server.
            client.send_str('OK')

            break

        # Connection with the server was refused.
        except ConnectionRefusedError:
            err = 'The connection with this server was refused!'

        # Connection timeout.
        except ConnectionTimeoutError:
            err = 'The connection attempt has timed out!'

        # Port is not valid.
        except InvalidPortError:
            err = 'Invalid port number!'

        # Unknown or nonexistent host.
        except UnknownHostError:
            err = 'Unknown host!'

        # Stops the feedback animation thread.
        thread.alive = False

        print(_lt(_lt(error(err))))
        press_enter_to('try again', F().red(), F().white())

    # Receives some informations and instructions from the server.
    client.log(client.recv_str())
    client.log(client.recv_str())

    # Opens a new speaker.
    with sd.OutputStream(blocksize=CHUNK_SIZE,
                         channels=CHANNELS,
                         dtype=np.int16,
                         samplerate=FRAME_RATE) as speaker:
        try:

            # Receives the first package.
            package = client.recv()

            # Wait for new packages from the server while they are not empty.
            while len(package) != 0:

                # Gets the audio from the package.
                received = M(modulation, package)

                # If the client chosen no modulated audio,...
                if modulation == NO_MOD:

                    # ... then just speaks the original package...
                    speaker.write(received.output())

                    # ... and receives the next one.
                    package = client.recv()

                    continue

                # Demodulates the received audio.
                demodulated = received.demodulate()

                # Filters the demodulated audio.
                filtered = demodulated.lowpass()

                # Outputs the filtered audio in the speaker.
                speaker.write(filtered.output())

                # Receives the next package.
                package = client.recv()

            # Logs the server shutdown.
            client.log(_ltb(label(error('The server has been shut down!'))))

        # The server has shut down.
        except ConnectionResetError:

            # Logs the server shutdown.
            client.log(_ltb(label(error('The server has been shut down!'))))

        # Ctrl+C pressed.
        except (EOFError, KeyboardInterrupt):

            # Logs the client disconnecting.
            client.log(_ltb(label(error('Disconnecting from the server...'))))

    # Disconnects from the server.
    client.disconnect()

    press_enter_to('back to the client menu', F().red(), F().white())


def set_name(client: Client, formatter: F = None) -> None:
    """
    "Change my name" client menu option.

    ---
    Arguments
    ---

        client (Client)
    The client instance which the name will be changed.

        formatter (Formatter, None)
    A Formatter to format some of the screen text.
    """

    # If a string Formatter was not provided,...
    if formatter is None:

        # ... instantiates a new one.
        formatter = F().magenta()

    # Asks the user for the client name until it is valid.
    while True:
        print(formatter.erase(title()))
        print(_l(formatter.erase('Choose how you want to be called.')))

        try:

            # Waits for the user to provide the client name.
            client.set_name(input(_lt('Your name: ')))

            break

        # Empty name.
        except InvalidNameError:
            err = 'You must provide a name!'

        print(_lt(error(err)))
        press_enter_to('try again', F().red(), F().white())
