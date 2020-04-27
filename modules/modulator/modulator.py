from __future__ import annotations

from typing import Union

from scipy.signal import firwin

from nptyping import Array

import numpy as np

from modules.audio.settings import CHANNELS, FRAME_RATE

from modules.modulator.constants import AM, AM_SC, NO_MOD

from modules.modulator.error import (InvalidModulationTypeError,
                                     InvalidSignalTypeError)

from modules.modulator.settings import AM_CARRIER_FREQ, CUTOFF


class Modulator():

    # Available modulation type list.
    modulations = [AM, AM_SC, NO_MOD]

    def __init__(self, modulation: str, signal: Union[bytes,
                                                      Array[int]]) -> None:
        """
        Instantiates a new modulator.

        ---
        Arguments
        ---

            modulation (str)
        A modulation type to use.

            signal Union(bytes, Array(int))
        A signal to set as this modulator signal.
        """

        # Attributes the modulation type.
        self.__set_modulation(modulation)

        # Sets the signal to modulate.
        self.__set_signal(signal)

    def demodulate(self) -> Modulator:
        """
        Demodulates a signal.

        ---
        Returns
        ---

            Modulator
        The instance itself.
        """

        # Amplitude Modulation.
        if self.__modulation == AM:

            # Demodulates the signal.
            self.__signal = np.abs(self.__signal)

        # Amplitude Modulation with Suppressed Carrier.
        elif self.__modulation == AM_SC:

            # Generates a carrier wave.
            carrier = self.__am_carrier()

            # Modulates the signal.
            self.__signal = np.multiply(self.__signal, carrier)

        # Returns the instance itself.
        return self

    def encode(self) -> bytes:
        """
        Converts the signal from NumPy array to byte buffer.

        ---
        Returns
        ---

            bytes
        The signal as a byte buffer.
        """

        # Returns the signal as a byte buffer.
        return self.__signal.astype(np.int16).tobytes()

    def lowpass(self) -> Modulator:
        """
        Applies a lowpass filter to the signal.

        ---
        Returns
        ---

            Modulator
        The instance itself.
        """

        # Replaces the signal with the filtered one.
        self.__signal = self.__lowpass(self.__signal)

        # Returns the instance itself.
        return self

    def modulate(self) -> Modulator:
        """
        Modulates a signal.

        ---
        Returns
        ---

            Modulator
        The instance itself.
        """

        # Amplitude Modulation.
        if self.__modulation == AM:

            # Generates a carrier wave.
            carrier = self.__am_carrier()

            # Modulates the signal.
            self.__signal = np.multiply(self.__signal, carrier)
            self.__signal = np.add(self.__signal, carrier)
            self.__signal = np.divide(self.__signal, 2)

        # Amplitude Modulation with Suppressed Carrier.
        elif self.__modulation == AM_SC:

            # Generates a carrier wave.
            carrier = self.__am_carrier()

            # Modulates the signal.
            self.__signal = np.multiply(self.__signal, carrier)

        # Returns the instance itself.
        return self

    def output(self) -> Array[float]:
        """
        Returns the unflatted NumPy array of the signal.

        ---
        Returns
        ---

            Array(float)
        The unflatted signal.
        """

        # Returns the unflatted signal.
        return np.reshape(self.__signal,
                          (len(self.__signal) // CHANNELS, CHANNELS)).astype(
                              np.int16)

    def __am_carrier(self) -> Array[float]:
        """
        Generates a carrier wave for amplitude modulation.

        ---
        Returns
        ---

            Array(float)
        The NumPy array of the generated carrier signal.
        """

        # Generates the time axis values.
        t = np.arange(len(self.__signal))

        # Returns a cosine wave with a frequency of `AM_CARRIER_FREQ` Hz.
        return np.cos(2 * np.pi * t * AM_CARRIER_FREQ)

    def __check_modulation(self, modulation: str) -> None:
        """
        Checks whether the modulation type is among those available.

        ---
        Arguments
        ---

            modulation (str)
        A modulation type to check.

        ---
        Raises
        ---

            InvalidModulationTypeError
        The modulation is not available.
        """

        # If the modulation is not in the modulation type list,...
        if modulation not in self.modulations:

            # ... raises an error.
            raise InvalidModulationTypeError(modulation)

    def __lowpass(self,
                  signal: Array[float],
                  cutoff: float = CUTOFF) -> Array[float]:
        """
        Applies a lowpass filter to a signal.

        ---
        Arguments
        ---

            signal (Array(float))
        A signal to filter.

            cutoff (float, CUTOFF)
        A cutoff frequency.

        ---
        Returns
        ---

            Array(float)
        The filtered signal.
        """

        # Generates a FIR low pass filter.
        lowpass = firwin(numtaps=len(signal),
                         cutoff=cutoff,
                         window='blackmanharris',
                         pass_zero='lowpass',
                         fs=FRAME_RATE)

        # Returns the filtered signal.
        return np.convolve(signal, lowpass, 'same')

    def __set_modulation(self, modulation: str) -> None:
        """
        Sets the modulation type to this modulator.

        ---
        Arguments
        ---

            modulation (str)
        A modulation type to set.
        """

        # Checks whether the modulation type is among those available.
        self.__check_modulation(modulation)

        # Attributes the modulation type.
        self.__modulation = modulation

    def __set_signal(self, signal: Union[bytes, Array[int]]) -> None:
        """
        Defines the signal of this modulator.

        ---
        Arguments
        ---

            signal (Union(bytes, Array(int)))
        A NumPy array signal to set.

        ---
        Raises
        ---

            InvalidSignalTypeError
        The signal is not a NumPy array.
        """

        # If `signal` is neither a byte buffer nor a NumPy array,...
        if not isinstance(signal, (bytes, np.ndarray)):

            # ... raises an error.
            raise InvalidSignalTypeError()

        # If `signal` is a byte buffer,...
        if isinstance(signal, bytes):

            # ... converts it to a NumPy array.
            signal = np.frombuffer(signal, np.int16)

        # Sets the signal to this modulator.
        self.__signal = signal.flatten()
