import re
import os


def get_int(prompt, lowest_valid=None, highest_valid=None):
    """
    Error traps an int between a range from the user.

    :param int lowest_valid: The lowest int that would be valid if None no lower bound
    :param int highest_valid: The highest int that would be valid if None no upper bound
    :param str prompt: The message shown to the user before taking input

    :return int: The number the user chose
    """
    while True:
        try:
            num = int(input(prompt))

            # Check if int is in the valid range
            # The upper and lower bounds are ignored if they are none
            if (lowest_valid and num < lowest_valid) or (highest_valid and num > highest_valid):
                if lowest_valid and highest_valid:
                    if lowest_valid == highest_valid:
                        print(f"Please enter {lowest_valid} as it is the only valid option")
                    else:
                        print(f"Please enter a number between {lowest_valid} and {highest_valid}")
                if not lowest_valid:
                    print(f"Please enter a number less than or equal to {highest_valid}")
                if not highest_valid:
                    print(f"Please enter a number greater than or equal to {lowest_valid}")

                continue

            return num
        except ValueError:
            print(f"Invalid input! Please enter a number")


def get_positive_number(prompt):
    """
    Error traps a positive number from the user.

    :param str prompt: The message shown to the user before taking input

    :return float: Positive number either decimal or whole or 0
    """
    while True:
        try:

            # Get input from the user
            user_input = input(prompt)

            # Convert the input to a float (can handle both integers and decimals)
            number = float(user_input)

            # Check if the number is 0 or greater
            if number >= 0:
                return number
            else:
                print("The number must be 0 or greater. Please try again.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def get_char(valid_chars, prompt):
    """
    Error traps a valid char from the user.

    :param str prompt: The message shown to the user before taking input
    :param str valid_chars: A string of all valid chars

    :return str: Valid char chosen by the user
    """
    while True:
        char = input(prompt)

        if len(char) != 1:
            print("Invalid input. Please enter just one character.")
        elif char not in valid_chars:
            print("Invalid input. Please enter only a valid character.")
        else:
            return char


def get_filename(prompt):
    """
    Error traps a valid filename from the user

    :param str prompt: The message shown to the user before taking input

    :return str: Valid filename
    """
    while True:
        filename = input(prompt)

        # Check for invalid characters using a regular expression
        if re.match(r'^[\w\-. ]+$', filename):
            return filename
        else:
            print("Invalid name. Please use letters, numbers, underscores, hyphens, periods, and spaces only.\n")


def get_path(prompt):
    """
    Error traps a valid path from the user that exists.
    If a file is included in the path ensures the file exists otherwise ensures the directory exists.

    :param str prompt: The message shown to the user before taking input

    :return str: Valid file path
    """
    while True:
        path = input(prompt)

        # Check for valid characters in the file path using a regular expression
        if re.match(r'^[\w\-. /\\:]+$', path):

            # Ensure that the path is either an existing file or directory
            if os.path.isfile(path) or os.path.isdir(path):
                return path
            else:
                print("The specified path does not exist. Please provide a valid file or directory path.")
        else:
            print("Invalid path. Please use letters, numbers, underscores, hyphens, periods, spaces, and valid path "
                  "separators (/, \\).")


def remove_timestamps(transcript):
    """
    Takes a transcript with timestamps and removes them.

    :param str transcript: The transcript with timestamps

    :return str: The transcript without the timestamps
    """

    # Define the regex pattern for the timestamp
    timestamp_pattern = r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*"

    # Replace all matches of the timestamp pattern with an empty string
    cleaned_text = re.sub(timestamp_pattern, '', transcript)

    return cleaned_text

def snake_to_title(snake_str):
    """
    Converts a snake_case word to Title Case.

    :param str snake_str: A snake_case string

    :return str: Title Case string
    """

    # Replace underscores with spaces
    title_str = snake_str.replace('_', ' ')

    # Capitalize the first letter and make the rest lowercase
    title_str = title_str.title()

    return title_str


def select_course_code(valid_course_codes, prompt):
    """
    Gets the user to select a course code form a set of valid course codes

    :param str prompt: The message shown to the user before taking input
    :param List[str] valid_course_codes: A list of valid course codes

    :return str: Course code selected by user
    """
    while True:
        course_code = input(prompt)

        if course_code in valid_course_codes:
            return course_code
        else:
            print("Invalid course code. Please select a course code which is already added.\n")

