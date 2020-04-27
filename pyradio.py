from emoji import emojize

from modules.formatter.formatter import Formatter as F

from modules.core.menu import client_option, server_option

from modules.utils.utils import (_l, _lt, _ltb, clear, error, label,
                                 press_enter_to, title)

try:
    while True:
        print(F().blue(title()))

        # Initial messages.
        print(_l(F().bold().blue('Welcome to PyRadio!')))
        print(_ltb('What will be the mode of this instance?'))

        # Defines the main menu options, with their respective methods.
        options = [['Server', 'server_option'], ['Client', 'client_option']]

        # Lists the options.
        for i, option in enumerate(options):
            print(_l(label(option[0], F().red(i + 1), F())))

        print(_l(label('Exit PyRadio', F().red(0), F())))

        # Reads the chosen option.
        try:
            opt = int(input(_lt('Your option: ')))

            # Checks whether the option is available.
            if opt not in range(0, len(options) + 1):
                raise ValueError()

        # Invalid or nonexistent option.
        except ValueError:
            print(_lt(error('Invalid option!')))
            press_enter_to('try again', F().red(), F().white())

            continue

        # If the option is 0, exit.
        if not opt:
            break

        # If no, runs the corresponding function.
        globals()[options[opt - 1][1]]()

# Ctrl+C pressed.
except (EOFError, KeyboardInterrupt):
    pass

try:
    print(F().blue(title()))

    # Acknowledgments and finishing the application.
    print(_l(F().bold().blue('Thank you very much for using PyRadio!')))

    # Credits, about and other stuffs.
    print(_lt(F().blue('Credits:')))

    print(_lt('2020 © Marlon Luís de Col'))
    print(_l('Computer Engineering'))
    print(_l('Unoesc Chapecó'))

    print(
        _lt(F().blue('Made with {} and {} in Brazil!'.format(
            emojize(':hot_beverage:'), emojize(':yellow_heart:')))))

    press_enter_to('finish', F().blue(), F().white())

    print()
    clear()

# Ctrl+C pressed.
except (EOFError, KeyboardInterrupt):
    pass
