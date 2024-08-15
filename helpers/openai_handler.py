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

    # Gets the summary and title from gpt
    summary_sheet = ask_gpt(
        system_prompt= ("You are a student that writes notes from a lecture based on a transcript."
                        "Your notes are to be written strictly in Markdown. The user will provide you with the "
                        "transcript."
                        "Strictly follow this Markdown template to format the note:\n\n"
                        "<!-- Add as many definitions as needed more is better -->\n"
                        "## Definitions\n\n"
                        "**Term 1**: Definition of term 1.\n\n"
                        "**Term 2**: Definition of term 2.\n\n"
                        "**Term 3**: Definition of term 3.\n\n"
                        "---\n\n"
                        "<!-- OPTIONAL: Only include this if applicable, but you may add more -->\n"
                        "## Important Formulas / Equations\n\n"
                        "**Formula name**: \( E = mc^2 \)\n\n"
                        "**Formula name**: \[ a^2 + b^2 = c^2 \]\n\n"
                        "**Formula name**: Make sure to include any other relevant equations.\n\n"
                        "---\n\n"
                        "<!-- Add as many Key Concepts as needed -->\n"
                        "## Summary of Key Concepts\n\n"
                        "**Key Concept 1**: Single paragraph summary of key concepts\n\n"
                        "**Key Concept 2**: Single paragraph summary of key concepts\n\n"
                        "**Key Concept 3**: Single paragraph summary of key concepts\n\n"
                        "**Key Concept 4**: Single paragraph summary of key concepts\n\n"
                        "---\n\n"
                        "<!-- OPTIONAL: Only include this if applicable, but you may add more -->\n"
                        "## Step-by-step examples\n\n"
                        "### Problem desc 1\n"
                        "**Step 1**: Step used in transcript\n\n"
                        "**Step 2**: Step used in transcript\n\n"
                        "**Step 3**: Step used in transcript\n\n"
                        "### Problem desc 2\n"
                        "**Step 1**: Step used in transcript\n\n"
                        "**Step 2**: Step used in transcript\n\n"
                        "**Step 3**: Step used in transcript\n\n"
                        "---\n\n"
                        "## Questions & Discussions\n\n"
                        "- **Question 1**: Important question or discussion point.\n"
                        "- **Question 2**: Another question or topic for discussion.\n\n"
                        "---\n\n"
                        "<!-- OPTIONAL: For example if there is a test on some day or any date mentioned for any "
                        "reason including past dates  -->\n"
                        "## Important Dates\n\n"
                        "- [ ] **Date 1**: Reason for importance\n"
                        "- [ ] **Date 2**: Reason for importance\n"
                        "- [ ] **Date 3**: Reason for importance\n"),
        user_prompt=transcript
    )

    sheet_title = ask_gpt(
        system_prompt=("Your a student that needs to write a brief one sentence title for a summary sheet."
                       "Your output will be converted directly into a filename so do not include quotes or any "
                       "characters like that. The user will provide you with the summary sheet"),
        user_prompt=summary_sheet
    )

    return summary_sheet, sheet_title

