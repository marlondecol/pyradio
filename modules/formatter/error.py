from typing import Any


class FormatsError(Exception):
    """
    Some fundamental Formatter's error.
    """


class InvalidColorError(FormatsError):
    def __init__(self, color: Any) -> None:
        """
        Color not present in the Formatter's color list.

        ---
        Arguments
        ---

            color (Any)
        The color tag of the attempt.
        """

        self.color = color

        super().__init__()


class InvalidStyleError(FormatsError):
    def __init__(self, style: Any) -> None:
        """
        Style not present in the Formatter's stye list.

        ---
        Arguments
        ---

            style (Any)
        The style tag of the attempt.
        """

        self.style = style

        super().__init__()


class InvalidTagError(FormatsError):
    def __init__(self, tag: Any) -> None:
        """
        Tag not present in the Formatter's tag list.

        ---
        Arguments
        ---

            tag (Any)
        The tag of the attempt.
        """

        self.tag = tag

        super().__init__()
