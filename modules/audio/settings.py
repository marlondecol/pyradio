"""
Default audio settings.
"""

import numpy as np

from modules.socket.settings import PACKAGE_SIZE

# Number of sound channels.
CHANNELS = 2

# The size of the streaming buffer, that needs to fit into the socket buffer.
CHUNK_SIZE = PACKAGE_SIZE // CHANNELS // np.dtype(np.int16).itemsize

# Sound device frame rate. In this case, 44.1 KHz.
FRAME_RATE = int(44.1e3)
