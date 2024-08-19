from colorama import Fore, Style

def print_title():
    """
    Prints Noter (title) in ascii

    :return: None
    """
    ascii_title = """
    888b    888          888                    
    8888b   888          888                    
    88888b  888          888                    
    888Y88b 888  .d88b.  888888 .d88b.  888d888 
    888 Y88b888 d88""88b 888   d8P  Y8b 888P"   
    888  Y88888 888  888 888   88888888 888     
    888   Y8888 Y88..88P Y88b. Y8b.     888     
    888    Y888  "Y88P"   "Y888 "Y8888  888     
    """

    print_green(ascii_title)


def print_green(text):
    """
    Takes text and prints it in green

    :param str text: Text to print

    :return: None
    """
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_red(text):
    """
    Takes text and prints it in red

    :param str text: Text to print

    :return: None
    """
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


def print_yellow(text):
    """
    Takes text and prints it in yellow

    :param str text: Text to print

    :return: None
    """
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")

