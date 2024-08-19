from helpers.input_safety import get_int, get_char


def main():
    """
    Renders the main menu for the user and returns a clean user choice.

    :return int: Menu choice
    """
    print("1. Record now")
    print("2. Transcribe and summarize from recording")
    print("3. Summarize from transcript")
    print("4. View summaries/transcripts/lecture recordings")
    print("5. Edit classes")
    print("6. Quit")

    return get_int(lowest_valid=1, highest_valid=6, prompt="")


def choose_class(course_codes, archived_codes=None):
    """
    Get user to select the class they want to use.

    :param List[str] archived_codes: A list of archived users courses
    :param List[str] course_codes: A list of all the users classes

    :return str: Course code
    :return bool: Weather or not its archived
    """
    print("\nSelect class:")

    # Prints all courses as options
    for i, course in enumerate(course_codes):
        print(f"{i + 1}. {course}")

    highest_valid = len(course_codes)

    # Optionally gives the option to view archived classes
    if archived_codes:
        highest_valid += 1
        print(f"{highest_valid}. Archived classes")

    # User selected the number they see beside their current course
    choice = get_int(lowest_valid=1, highest_valid=highest_valid, prompt="")

    # Choose archived classes
    if choice == highest_valid and archived_codes:
        print("\nSelect an archived class:")

        # Prints all archived courses as options
        for i, course in enumerate(archived_codes):
            print(f"{i + 1}. {course}")
            class_choice = get_int(lowest_valid=1, highest_valid=len(archived_codes), prompt="")

            return archived_codes[class_choice - 1], True

    # Return the name of the course
    return course_codes[choice - 1], False


def manage_live_recording():
    """
    Get user to select menu option for live recording.

    :return str: User's (single character) choice
    """
    print("\nc - to transcribe the recording till this point (does not stop recording)")
    print("s - to stop recording")
    choice = get_char(valid_chars="sc", prompt="")

    return choice


def select_media_type():
    """
    Get user to select a media type from our available files.

    :return str: The folder name of user's choice
    """
    print("\nSelect media type:")
    print("1. Summary Sheet")
    print("2. Transcript")
    print("3. Lecture Recordings")

    choice = get_int(lowest_valid=1, highest_valid=3, prompt="")

    match choice:
        case 1:
            return "summaries"
        case 2:
            return "transcripts"
        case 3:
            return "lectures"


def edit_class_options():
    """
    Get user to select the type of edit type wish to make.

    :return str: The type of edit
    """
    print("\nSelect option:")
    print("1. Archive classes")
    print("2. Add new classes")
    print("3. New semester (archive all current classes and add new classes)")
    print("4. Restore from archive")

    choice = get_int(lowest_valid=1, highest_valid=4, prompt="")

    match choice:
        case 1:
            return "archive"
        case 2:
            return "add_classes"
        case 3:
            return "new_semester"
        case 4:
            return "restore_from_archive"

