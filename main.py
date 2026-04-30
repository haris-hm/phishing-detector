import requests
import json
import re
import sys

from requests import Response
from re import Match

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phishing-detector"
SUCCESS_RETURN = 0
EXIT_RETURN = 1
ERROR_RETURN = 2


class AnalyzerResponse:
    def __init__(self, return_code: int, analysis: str = ""):
        self.analysis: str = analysis
        self.return_code: int = return_code


def ask_model(input_prompt: str) -> str:
    res: Response = requests.post(
        url=OLLAMA_URL, json={"model": MODEL, "prompt": input_prompt, "stream": False}
    )

    return res.json()["response"].strip()


def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def analyze_email(
    sender_name: str, sender_address: str, subject_line: str, email_body: str
) -> str:
    if not validate_email(sender_address):
        raise ValueError("Invalid email address format")

    if not sender_name or not subject_line or not email_body:
        raise ValueError("Sender name, subject line, and email body cannot be empty")

    input_prompt: str = f"""
    Sender: {sender_name} <{sender_address}>
    Subject Line: {subject_line}

    {email_body}
    """

    return ask_model(input_prompt)


def prompt_email() -> AnalyzerResponse:
    sender: str = ""
    sender_address: str = ""
    subject_line: str = ""
    email_body: str = ""

    while not sender:
        sender = input("What is the sender's name?\n")
        if sender == "/exit":
            return AnalyzerResponse(EXIT_RETURN)

    while not sender_address:
        sender_address = input("What is the sender's email address?\n")
        if sender_address == "/exit":
            return AnalyzerResponse(EXIT_RETURN)

    while not subject_line:
        subject_line = input("What is the email's subject line?\n")
        if subject_line == "/exit":
            return AnalyzerResponse(EXIT_RETURN)

    while not email_body:
        print(
            "What is the email's body?\nPaste/Enter text and press Ctrl+D (Unix) or Ctrl+Z (Win) to end:"
        )
        email_body: str = sys.stdin.read()

        if email_body == "/exit":
            return AnalyzerResponse(EXIT_RETURN)

    print("Analyzing email, please wait...")

    try:
        analysis: str = analyze_email(sender, sender_address, subject_line, email_body)
        return AnalyzerResponse(SUCCESS_RETURN, analysis)
    except ValueError as e:
        print(f"Error: {e}")
        return AnalyzerResponse(ERROR_RETURN)


def display_analysis(analysis: str) -> bool:
    match: Match[str] | None = re.search(r"\{.*\}", analysis, re.DOTALL)

    if not match:
        print("Something went wrong during analysis, please try again...")
        return False

    response_json = json.loads(match.group(0))
    analysis: str = response_json.get("analysis", "No analysis provided.")
    phishing_probability: float = response_json.get("phishing_probability", 0.0)

    print("\n\n--- Analysis Result ---")
    print(f"Analysis: {analysis}")
    print(f"Phishing Probability: {phishing_probability:.2%}")
    print("-----------------------\n\n")
    return True


def main():
    print("Welcome to the phishing detector!")
    print("Type /exit at any point to exit the program.")

    while True:
        response: AnalyzerResponse = prompt_email()

        if response.return_code == EXIT_RETURN:
            return

        if response.return_code == ERROR_RETURN:
            continue

        if not display_analysis(response.analysis):
            continue


if __name__ == "__main__":
    main()
