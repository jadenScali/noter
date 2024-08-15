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

    return get_int(lowest_valid=1, highest_valid=6, prompt="")

def choose_class(course_codes):
    """
    Get user to select the class they want to use

    :param List[str] course_codes: A list of all the users classes

    :return: Course code str
    """
    print("Select class:")

    # Prints all courses as options
    for i, course in enumerate(course_codes):
        print(f"{i + 1}. {course}")

    # User selected the number they see beside their current course
    choice = get_int(lowest_valid=1, highest_valid=len(course_codes), prompt="")

    # Return the name of the course
    return course_codes[choice - 1]


