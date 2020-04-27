from socket import socket

import numpy as np

import sounddevice as sd

from modules.audio.settings import CHANNELS, CHUNK_SIZE, FRAME_RATE

from modules.formatter.formatter import Formatter as F

from modules.modulator.constants import NO_MOD

from modules.modulator.modulator import Modulator as M

from modules.socket.error import ClientDisconnectedError, SocketError

from modules.socket.server import Server

from modules.utils.utils import _lt, label, title


def handle_client(server: Server, client: socket) -> None:
    """
    Handles a connected client.

    ---
    Arguments
    ---

        server (Server)
    A server instance.

        client (socket)
    A client socket instance that will be handled.
    """

    # Gets the client address.
    host, port = server.address(client)

    # Gets the color that the client has received.
    color = server.get_color(client)

    # Formats the client name for sending.
    nick = F().bold().paint(color, server.get_name(client))

    # If this server does not receive a client confirmation,...
    if server.recv_str(client) != 'OK':

        # ... then says bye to him.
        server.bye(client)

        # Logs the event.
        server.log(
            _lt(F().yellow(
                label('{} left the server ({}:{})'.format(nick, host, port)))))

    # Gets the modulation the customer has chosen.
    modulation = server.get_modulation(client)

    # Logs the connection event.
    server.log(
        _lt(F().magenta(
            label('{} just connected{}! ({}:{})'.format(
                nick, ' in {}'.format(modulation.upper())
                if modulation != NO_MOD else '', host, port)))))

    # Sends some informations and instructions to the client.
    server.send_str(client,
                    F().paint(color, title(clear_screen=False)).render())
    server.send_str(
        client,
        _lt(label(F().bold().green('Welcome to PyRadio, {}!'.format(nick)))))
    server.send_str(
        client, _lt(F().cyan(label('Your address is {}:{}'.format(host,
                                                                  port)))))
    server.send_str(
        client,
        _lt(F().cyan(
            label('Listening {} modulation'.format('in {}'.format(
                modulation.upper()) if modulation != NO_MOD else 'without')))))
    server.send_str(
        client,
        _lt(label(F().bold().blue('You can press Ctrl+C to disconnect'))))

    # Opens the microphone.
    with sd.InputStream(blocksize=CHUNK_SIZE,
                        channels=CHANNELS,
                        dtype=np.int16,
                        samplerate=FRAME_RATE) as microphone:
        try:

            # Sends the sound to the client while the server is connected.
            while True:

                # Records the audio from the microphone.
                recorded = M(modulation, microphone.read(CHUNK_SIZE)[0])

                # If the client chosen no modulated audio,...
                if modulation == NO_MOD:

                    # ... then just sends the pure recorded audio.
                    server.send(client, recorded.encode())

                    continue

                # Filters the recorded audio.
                filtered = recorded.lowpass()

                # Modulates the filtered audio.
                modulated = filtered.modulate()

                # Sends the modulated audio.
                server.send(client, modulated.encode())

        # Disconnected client.
        except ClientDisconnectedError:

            # Gets the client address.
            host, port = server.address(client)

            # Gets the color that the client has received.
            color = server.get_color(client)

            # Formats the client name for sending.
            nick = F().bold().paint(color, server.get_name(client))

            # Say bye to him.
            server.bye(client)

            # Logs the event.
            server.log(
                _lt(F().yellow(
                    label('{} left the server ({}:{})'.format(
                        nick, host, port)))))

        # The server has sut down.
        except SocketError:
            pass
