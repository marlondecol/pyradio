from __future__ import annotations

from modules.formatter.colors import (BLACK, BLUE, CYAN, GREEN, MAGENTA, RED,
                                      WHITE, YELLOW)

from modules.formatter.constants import END

from modules.formatter.error import (InvalidColorError, InvalidStyleError,
                                     InvalidTagError)

from modules.formatter.styles import (BACKGROUND, BLINK, BOLD, FADED, ITALIC,
                                      STRIKE, UNDERLINE)


class Formatter:

    # Available color tag list.
    __colors = [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]

    # Available style tag list.
    __styles = [BACKGROUND, BLINK, BOLD, FADED, ITALIC, STRIKE, UNDERLINE]

    def __init__(self, string: str = '') -> None:
        """
        Instantiates a brand new string formatter.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.
        """

        # Sets new attributes.
        self.clear()

        # Writes the string, if provided.
        self.write(string)

    def __str__(self) -> str:
        """
        Called when printing this instance.

        ---
        Returns
        ---

            str
        The formatted string.
        """

        # Returns the formatted string.
        return self.render()

    def background(self, color: str = None, string: str = '') -> Formatter:
        """
        Paints the background.

        ---
        Arguments
        ---

            color (str, None)
        A color for the background.

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the background and then returns the instance itself.
        return self.paint(color).style(BACKGROUND, string)

    def black(self, string: str = '') -> Formatter:
        """
        Paints with a black foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(BLACK, string)

    def blink(self, string: str = '') -> Formatter:
        """
        Makes the string blink.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(BLINK, string)

    def blue(self, string: str = '') -> Formatter:
        """
        Paints with a blue foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(BLUE, string)

    def bold(self, string: str = '') -> Formatter:
        """
        Applies bold style to the string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(BOLD, string)

    def check_color(self, color: str) -> None:
        """
        Checks whether the color tag is among those available.

        ---
        Arguments
        ---

            color (str)
        A color tag to check.

        ---
        Raises
        ---

            InvalidColorError
        The color tag is not available.
        """

        # If the color tag is not in the color list,...
        if color not in self.__colors:

            # ... raises an error.
            raise InvalidColorError(color)

    def check_style(self, style: str) -> None:
        """
        Checks whether the style tag is among those available.

        ---
        Arguments
        ---

            style (str)
        A style tag to check.

        ---
        Raises
        ---

            InvalidColorError
        The style tag is not available.
        """

        # If the style tag is not in the style list,...
        if style not in self.__styles:

            # ... raises an error.
            raise InvalidStyleError(style)

    def check_tag(self, tag: str) -> None:
        """
        Checks whether the tag is among those available.

        ---
        Arguments
        ---

            tag (str)
        A tag to check.

        ---
        Raises
        ---

            InvalidColorError
        The tag is not available.
        """

        # If the tag is not in the color or style list,...
        if tag not in self.__colors + self.__styles:

            # ... raises an error.
            raise InvalidTagError(tag)

    def clear(self) -> Formatter:
        """
        Resets the string and clean the format stack.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Resets the formatted string.
        self.__string = ''

        # Unpacks the applied formats.
        self.__stack = []

        # Returns the instance itself.
        return self

    def cyan(self, string: str = '') -> Formatter:
        """
        Paints with a cyan foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(CYAN, string)

    def end(self, string: str = '') -> Formatter:
        """
        Closes the last format.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Adds the END tag, writes the string and returns the instance itself.
        return self.write(END).write(string)

    def erase(self, string: str = '') -> Formatter:
        """
        Resets just the string.

        ---
        Arguments
        ---

            string (str, '')
        Some text to format.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Resets the formatted string.
        self.__string = ''

        # For each stacked format,...
        for tag in self.__stack:

            # ... checks if it is valid...
            self.check_tag(tag)

            # ... and writes it to the formatted string.
            self.write(tag)

        # Then, writes the string and returns the instance itself.
        return self.write(string)

    def faded(self, string: str = '') -> Formatter:
        """
        Applies faded color style to the string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(FADED, string)

    def green(self, string: str = '') -> Formatter:
        """
        Paints with a green foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(GREEN, string)

    def italic(self, string: str = '') -> Formatter:
        """
        Applies italic style to the string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(ITALIC, string)

    def magenta(self, string: str = '') -> Formatter:
        """
        Paints with a magenta foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(MAGENTA, string)

    def paint(self, color: str = None, string: str = '') -> Formatter:
        """
        Paints the string with some color.

        ---
        Arguments
        ---

            color (str, None)
        A color to paint.

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # If a color was provided,...
        if color is not None:

            # ... checks if it is valid.
            self.check_color(color)

        # Pushes the color tag to the format stack and returns the instance
        # itself.
        return self.push(color, string)

    def pop(self, string: str = '') -> Formatter:
        """
        Unstacks the last format from the stack.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Pops the last tag from the format stack.
        last = self.__stack.pop()

        # If the BACKGROUND tag was the last,...
        if last == BACKGROUND:

            # ... then it should pops the second last, which is a color tag.
            self.__stack.pop()

        # Continues the string and returns the instance itself.
        return self.end(''.join(self.__stack)).write(string)

    def print(self) -> None:
        """
        Directly prints the formatted string.
        """

        # Just prints the instance itself.
        print(self)

    def push(self, tag: str = None, string: str = '') -> Formatter:
        """
        Stacks a formatted tag to the stack.

        ---
        Arguments
        ---

            tag (str, None)
        A tag to push in.

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # If a tag was provided,...
        if tag is not None:

            # ... checks if it is valid.
            self.check_tag(tag)

            # If it is equal to the last one,...
            if len(self.__stack) != 0 and tag == self.__stack[-1]:

                # ... the pops it from the stack.
                return self.pop(string)

            # If no, pushes the tag to the format stack,...
            self.__stack.append(tag)

            # ... and writes it.
            self.write(tag)

        # Writes the provided string and returns the instance itself.
        return self.write(string)

    def red(self, string: str = '') -> Formatter:
        """
        Paints with a red foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(RED, string)

    def render(self) -> str:
        """
        Returns the formatted string.

        ---
        Returns
        ---

            str
        The formatted string.
        """

        # Returns the formatted string, followed by the END tag.
        return self.__string + END

    def reset(self, string: str = '') -> Formatter:
        """
        Reset both the string and stack attributes.

        ---
        Arguments
        ---

            string (str, '')
        Som string to format.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Clean the format stack.
        self.__stack.clear()

        # Closes the format string and returns the instance itself.
        return self.end(string)

    def strike(self, string: str = '') -> Formatter:
        """
        Applies a strike to the string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(STRIKE, string)

    def string(self) -> str:
        """
        Returns the formatted string without the END tag.

        ---
        Returns
        ---

            str
        Just the string as is.
        """

        # Returns the string as is.
        return self.__string

    def style(self, style: str = None, string: str = '') -> Formatter:
        """
        Stylizes the string with some style.

        ---
        Arguments
        ---

            style (str, None)
        A style tag.

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # If a style tag was provided,...
        if style is not None:

            # ... checks if it is valid.
            self.check_style(style)

        # Pushes the style tag to the format stack and returns the instance
        # itself.
        return self.push(style, string)

    def underline(self, string: str = '') -> Formatter:
        """
        Applies an underline to the string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Stylizes the string and then returns the instance itself.
        return self.style(UNDERLINE, string)

    def white(self, string: str = '') -> Formatter:
        """
        Paints with a white foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(WHITE, string)

    def write(self, string: str = '') -> Formatter:
        """
        Adds some string to the formatted string.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Makes a string  from the current tags.
        tags = ''.join(self.__stack)

        # Checks whether the string is, actually, another Formatter instance.
        if isinstance(string, Formatter):

            # Splits the string between the END tags.
            strings = string.string().split(END)

            # Joins the strings with all of the pre-existing formats.
            return self.write((END + tags).join(strings)).end(tags)

        # Does not forget any previous format.
        self.__string += (END + tags).join(str(string).split(END))

        # Returns the instance itself.
        return self

    def yellow(self, string: str = '') -> Formatter:
        """
        Paints with a yellow foreground.

        ---
        Arguments
        ---

            string (str, '')
        Some string to add.

        ---
        Returns
        ---

            Formatter
        The instance itself.
        """

        # Paints the foreground and then returns the instance itself.
        return self.paint(YELLOW, string)
