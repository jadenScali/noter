from openai import OpenAI
from dotenv import dotenv_values

# Load the .env file into a dictionary
config = dotenv_values(".env")

# Set api_key for openai
client = OpenAI(api_key=config["OPENAI_API_KEY"])


def ask_gpt(system_prompt, user_prompt):
    """
    Sends a request to gpt4-o with custom system and user prompt.

    :param str system_prompt: Used to give instructions of the task
    :param str user_prompt: Used to give context for the task

    :return: Response from gpt4-o as a str
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return completion.choices[0].message.content


def summary_sheet_gpt(transcript):
    """
    Creates summary sheet based on a lecture transcript

    :param str transcript: Transcript of a lecture

    :return: A str (.md compatible) summary sheet
    :return: A str title for the summary sheet
    """

    note_template = """
    <!-- Add every definition given in the lecture unlimited -->
    ## Definitions 👩🏻‍🏫

    **Recursion**: is a technique where a function calls itself directly or indirectly to solve a problem. A recursive function typically solves a problem by reducing it to a smaller instance of the same problem, which is solved in the same way, until it reaches a base case.

    **Photosynthesis**: is the process by which green plants, algae, and some bacteria convert light energy, usually from the sun, into chemical energy stored in molecules such as glucose. This process is fundamental to life on Earth as it is the primary source of organic matter for almost all organisms and releases oxygen into the atmosphere as a byproduct.

    **Term**: Definition of the term.

    ---
    
    <!-- OPTIONAL: For every relevant code syntax mentioned in the lecture unlimited -->
    ## Important Code snippets 💾
    
    **For loop**: Iterates over a sequence, such as a list or a range of numbers. 
    
        for item in items:
            print(item)
    
    **SELECT**: A statement in SQL is used to query data from a database.
        
        SELECT name FROM people;
    
    **Bubble sort**: a simple sorting algorithm that repeatedly steps through a list, compares adjacent elements, and swaps them if they are in the wrong order. This process continues until the list is sorted.
        
        def bubble_sort(arr):
        n = len(arr)
    
        # Traverse through all elements in the array
        for i in range(n):
    
            # Track if a swap was made in this pass
            swapped = False
            
            # Last i elements are already sorted, so we can skip them
            for j in range(0, n - i - 1):
    
                # Compare adjacent elements
                if arr[j] > arr[j + 1]:
    
                    # Swap if the element found is greater than the next element
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            
            # If no elements were swapped, the array is already sorted
            if not swapped:
                break
    
        # Example usage
        arr = [5, 3, 8, 4, 2]
        bubble_sort(arr)
        print("Sorted array:", arr)
    
    ---

    <!-- OPTIONAL: For every relevant formula mentioned in the lecture unlimited -->
    ## Important Formulas / Equations 🧮

    **Mass-Energy Equivalence**: \\[ E = mc^2 \\]

    **Pythagorean Theorem**: \\[ a^2 + b^2 = c^2 \\]

    **Formula name**: latex formula

    ---

    <!-- Add as many Key Concepts as needed unlimited -->
    ## Summary of Key Concepts 🔑

    **Key Concept Name 1**: Single paragraph summary of key concepts

    **Key Concept Name 2**: Single paragraph summary of key concepts

    **Key Concept Name 3**: Single paragraph summary of key concepts

    **Key Concept Name 4**: Single paragraph summary of key concepts

    ---

    <!-- OPTIONAL: For every example given in the lecture show the exact steps taken in class -->
    ## Step-by-step examples 😇

    ### Printing dog in Python
    **1. Define the Function** Use the def keyword to define a function. Name the function then add a parameter to the function to specify how many times to print "dog".

        def print_dog(n):


    **2. Implement a Loop** Use a for loop to repeat the printing process.

        def print_dog(n):
            for i in range(n):
                print("dog")

    **3. Call the function**: Call the function with a specific number to see the output.

        print_dog(5)

    ### Problem desc
    **1. Step name**: Step-by-step used in lecture

    **2. Step name**: Step-by-step used in lecture

    **n. Step name**: Step-by-step used in lecture

    ---

    <!-- OPTIONAL: For every question asked in class describe it and the professors response  -->
    ## Questions & Discussions 🙋🏼

    **What is the derivative of the function \\(f(x) = 3x^4 - 5x^2 + 2x - 7\\)?**
    To find the derivative of the function \\(f(x) = 3x^4 - 5x^2 + 2x - 7\\), we will use the power rule, which states that the derivative of \\(x^n\\) is \\(nx^{n-1}\\$. 

    Now let's differentiate each term:

    1. The derivative of \\(3x^4\\) is \\(12x^3\\) (using the power rule: \\(4 \\times 3 = 12\\) and decrease the exponent by 1).
    2. The derivative of \\(-5x^2\\) is \\(-10x\\) (again, using the power rule: \\(2 \\times -5 = -10\\)).
    3. The derivative of \\(2x\\) is \\(2\\) (the derivative of \\(x\\) is \\(1\\), so \\(2 \\times 1 = 2\\)).
    4. The derivative of a constant \\(-7\\) is \\(0\\).

    Putting it all together, the derivative \\(f'(x)\\) is:
    \\[
    f'(x) = 12x^3 - 10x + 2
    \\]

    So the final answer is \\(f'(x) = 12x^3 - 10x + 2\\).
    **Question?**
    Answer given in lecture

    ---

    <!-- OPTIONAL: For example if there is a test on some day or any date mentioned for any reason including past dates  -->
    ## Important Dates 🗓️

    - [ ] **Date 1**: Reason for importance
    - [ ] **Date 2**: Reason for importance
    - [ ] **Date 3**: Reason for importance

    ## Detailed summary 🧑🏽‍🎓

    A summary of everything covered about or touched upon in the entire lecture in chronological order
    """

    # Gets the summary and title from gpt
    summary_sheet = ask_gpt(
        system_prompt=  f"You are a student that writes notes from a lecture based on a transcript. "
                        f"The user will provide you with the transcript. Make sure you only include things from the "
                        f"transcript in the summary. "
                        f"Strictly follow this Markdown template to format the note:\n\n{note_template}",
        user_prompt=transcript
    )

    sheet_title = ask_gpt(
        system_prompt=("Your a student that needs to write a brief one or two word title for a summary sheet in "
                       "snake_case. Something that represents the text. The user will provide you with the "
                       "summary sheet"),
        user_prompt=summary_sheet
    )

    return summary_sheet, sheet_title

