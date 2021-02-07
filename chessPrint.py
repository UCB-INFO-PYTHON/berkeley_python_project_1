import os

# to ensure color works on certain systems,
os.system("")

class screenPrinter():
    """Class for printing text in pretty colors using ANSI escape codes"""

    CEND = '\33[0m'

    @staticmethod
    def printGreen(string, end='\n'):
        print('\33[32;1m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printBlackOnWhite(string, end='\n'):  # black on white
        print('\33[30;1m\33[47;1m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printYellow(string, end='\n'):    # yellow on black
        print('\33[33;1m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printCyan(string, end='\n'):
        print('\33[96m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printCyanOnWhite(string, end='\n'):  # black on white
        print('\33[96;1m\33[47;1m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printViolet(string, end='\n'):
        print('\33[95m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printGray(string, end='\n'):
        print('\33[90m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printRed(string, end='\n'):
        print('\33[31;1m' + string + screenPrinter.CEND, end=end)

    @staticmethod
    def printReplace(string, end='\n'):
        print(string.replace('YELLOW', '\33[33;1mYELLOW\33[0m').replace('GREEN', '\33[32;1mGREEN\33[0m' ), end)
