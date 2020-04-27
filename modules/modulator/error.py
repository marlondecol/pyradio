from typing import Any


class ModulatorError(Exception):
    """
    Some fundamental modulator error.
    """


class InvalidModulationTypeError(ModulatorError):
    def __init__(self, modulation: Any) -> None:
        """
        Modulation type is not present in the modulation type list.

        ---
        Arguments
        ---

            modulation (Any)
        The modulation type of the attempt.
        """

        self.modulation = modulation

        super().__init__()


class InvalidSignalTypeError(ModulatorError):
    """
    Unexpected data type for a signal.
    """
