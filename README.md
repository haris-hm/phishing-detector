# CYB 140 - Assignment 11: Phishing Detector

A phishing detector which uses a local Ollama model in order to analyze emails for potential threats. Created for the final assignment in Cybersecurity 140 at Drake University.

## Setting Up Model

Steps:

1. Have Ollama installed
2. Navigate to this repo's directory in the terminal
3. Run the following to create the custom model: `ollama create phishing-detector -f Modelfile`.
   - This will automatically pull the necessary model if needed and set up the custom model used by the script

## Running the script

Ensure that you have Python and pip installed, and that the `requests` module installed. If not installed, run `pip install requests` or activate a virtual environment by doing the following:

1. Create a virtual environment in the project directory using `python -m venv .venv`
2. Activate the virtual environment by running `source .venv/bin/activate`
3. Install dependencies using `pip install .`
4. Run the script by running `python main.py`

## Using the Detector

The detector needs the sender's name and email address, the email's subject line, and the email body. When running the script, enter each piece of information when prompted. In order to exit the script, type `/exit` at any time, or just press `Ctrl+C`.
