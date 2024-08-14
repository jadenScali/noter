import re

def get_int(lowest_valid, highest_valid, prompt):
    """
    Error traps an int between a range from the user

    :param int lowest_valid: The lowest int that would be valid
    :param int highest_valid: The highest int that would be valid
    :param str prompt: The message shown to the user before taking input

    :return: User chosen int
    """
    while True:
        try:
            num = int(input(prompt))

            # Check if int is in the valid range
            if num < lowest_valid or num > highest_valid:
                print(f"Please enter a number between {lowest_valid} and {highest_valid}")
                continue

            return num
        except ValueError:
            print(f"Invalid input! Please enter a number")


def get_filename(prompt):
    """
    Error traps a valid filename from the user

    :param prompt: The message shown to the user before taking input

    :return: Valid filename string
    """
    while True:
        filename = input(prompt)

        # Check for invalid characters using a regular expression
        if re.match(r'^[\w\-. ]+$', filename):
            return filename
        else:
            print("Invalid name. Please use letters, numbers, underscores, hyphens, periods, and spaces only.")

