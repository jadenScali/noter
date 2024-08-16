from helpers.input_safety import get_int, get_char


def main():
    """
    Renders the main menu for the user and returns a clean user choice

    :return: Menu choice int
    """
    print("1. Record now")
    print("2. Transcribe from recording")
    print("3. Summarize from transcript")
    print("4. View summaries/transcripts/lecture recordings")
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


def manage_live_recording():
    """
    Get user to select menu option for live recording.

    :return: User's str (single character) choice
    """
    print("c - to transcribe the recording till this point (does not stop recording)")
    print("s - to stop recording")
    choice = get_char(valid_chars="sc", prompt="")

    return choice


def select_media_type():
    """
    Get user to select a media type from our available files.

    :return: The folder name str of user's choice
    """
    print("Select media type:")
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

