"""
Default settings for socket connections.
"""

from modules.formatter.modules.colors import (BLUE, CYAN, GREEN, MAGENTA, RED,
                                              YELLOW)

# Maximum time for a connection attempt by a client, in seconds.
ATTEMPT_TIME = 3

# Number of unaccepted connections that the system will allow before refusing
# new connections.
BACKLOG_SIZE = 10

# Available client colors.
COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

# Default hostname.
DEFAULT_HOST = '127.0.0.1'

# Default port number.
DEFAULT_PORT = 33000

# String messages encoding.
ENCODING = 'utf-8'

# Transmission package size. In this case, 4 KB.
PACKAGE_SIZE = 1024 * 4
