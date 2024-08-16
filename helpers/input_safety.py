import re
import os


def get_int(lowest_valid, highest_valid, prompt):
    """
    Error traps an int between a range from the user.

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


def get_positive_number(prompt):
    """
    Error traps a positive number from the user

    :param str prompt: Prompt to ask users
    :return: Positive number either decimal or whole or 0
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
                print("The number must be 0 or greater. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

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


def get_path(prompt):
    """
    Error traps a valid file path from the user.

    :param str prompt: The message shown to the user before taking input

    :return: Valid file path string
    """
    while True:
        path = input(prompt)

        # Check for valid characters in the file path using a regular expression
        if re.match(r'^[\w\-. /\\:]+$', path):

            # Ensure that the path is a valid existing directory or can be created
            if os.path.exists(os.path.dirname(path)) or os.path.dirname(path) == '':
                return path
            else:
                print("The directory does not exist. Please provide a valid path.")
        else:
            print("Invalid path. Please use letters, numbers, underscores, hyphens, periods, spaces, and valid path "
                  "separators (/, \\).")


def remove_timestamps(transcript):
    """
    Takes a transcript with timestamps and removes them

    :param transcript: The transcript with timestamps
    :return: The str transcript without the timestamps
    """

    # Define the regex pattern for the timestamp
    timestamp_pattern = r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*"

    # Replace all matches of the timestamp pattern with an empty string
    cleaned_text = re.sub(timestamp_pattern, '', transcript)

    return cleaned_text

def snake_to_title(snake_str):
    """
    Converts a snake_case word to Title Case

    :param str snake_str: A snake_case string

    :return: Title Case string
    """
    # Replace underscores with spaces
    title_str = snake_str.replace('_', ' ')

    # Capitalize the first letter and make the rest lowercase
    title_str = title_str.title()

    return title_str

