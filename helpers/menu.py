from helpers.input_safety import get_int

def main():
    """
    Renders the main menu for the user and returns a clean user choice

    :return: Menu choice int
    """
    print("\n1. Record now")
    print("2. Transcribe from recording")
    print("3. View transcripts")
    print("4. View summaries")
    print("5. Edit classes")
    print("6. Quit")

    get_int(lowest_valid=1, highest_valid=6, prompt="")

