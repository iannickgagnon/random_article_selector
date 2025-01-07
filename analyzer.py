# External libraries
import os
import re
import json
import openai
from PyPDF2 import PdfReader

# Import prompts
from prompts import PROMPT_SYSTEM, PROMPT_USER

def calculate_nb_questions(questions_text):
    """
    Calculate the number of questions in the questions text.

    It assumes that each question starts with a label like 'A1.', 'B1.', etc.

    Args:
        questions_text (str): Text containing the questions.

    Returns:
        list: List of question keys (e.g., ['A1', 'A2', 'B1', 'B2']).
    """
    # Extract question labels by identifying lines that end with a period (e.g., 'A1.', 'B1.')
    return [line.split()[0][:-1] for line in questions_text.strip().split("\n") if line.strip() and line.split()[0][-1] == "."]

def extract_text_from_pdf(pdf_path):
    """
    Extracts the text content of a specified PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Text extracted from the PDF file.
    """
    try:
    
        # Initialize the PDF reader and concatenate text from all pages
        reader = PdfReader(pdf_path)
        text = "".join([page.extract_text() for page in reader.pages])

        # Make sure it is not ASCII-encoded
        if len(re.findall(r'\/C\d+', text)) > 100:
            text = re.sub(r'\/C\d+', lambda x: chr(int(x.group()[2:])), text)

        return text
    
    except Exception as err:
        # Handle errors during PDF reading
        print(f"\033[91mError reading {pdf_path}: {err}\033[0m")
        return ""

def send_to_chatgpt(pdf_text, prompt_system=PROMPT_SYSTEM, prompt_user=PROMPT_USER):
    """
    Sends the extracted text from a PDF to ChatGPT for evaluation.

    Args:
        pdf_text (str): Text extracted from the PDF.
        prompt_system (str): System-level prompt for ChatGPT.
        prompt_user (str): User-level prompt for ChatGPT.

    Returns:
        str: Response from ChatGPT.
    """
    try:
        # Use OpenAI API to get a response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": f"{prompt_user}\n\n{pdf_text}"}
            ],
            temperature=0.0,
        )
        return response.choices[0].message['content']
    except Exception as e:
        # Handle errors during API communication
        print(f"Error sending to ChatGPT: {e}")
        return ""

def analyze_pdfs(input_folder: str, output_folder: str = None):
    """
    Process the PDF files in the input folder by extracting the text, sending it to ChatGPT, and saving the results.

    Args:
        input_folder (str): Path to the input folder containing the PDF files.
        output_folder (str, optional): Path to the output folder to save the results. Defaults to None (same as input folder).

    Returns:
        None
    """

    # Set the output folder to the input folder if not specified
    if not output_folder:
        output_folder = input_folder

    # Check if the input folder is empty
    if not os.listdir(input_folder):
        print("\033[91mNo PDF files found in the input folder.\033[0m")
        return

    # Ensure the output folder is empty before proceeding
    if os.listdir(output_folder):
        print("\033[91mThe output folder is not empty. Please clear it before running the script.\033[0m")
        return

    # Get the list of question keys (e.g., ['A1', 'A2', 'B1'])
    questions_keys = calculate_nb_questions(PROMPT_USER)
    total_files = len([f for f in os.listdir(input_folder) if f.endswith(".pdf")])

    # Initialize result dictionaries
    results = {}
    aggregate_results = {}
    for key in questions_keys:
        aggregate_results[f'{key}_true'] = 0
        aggregate_results[f'{key}_false'] = 0
        aggregate_results[f'{key}_na'] = 0
        aggregate_results[f'{key}_total'] = 0

    # Process each PDF file
    for i, filename in enumerate(os.listdir(input_folder)):
        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_folder, filename)
        progress_pct = ((i + 1) / total_files) * 100
        print(f"\033[92m{progress_pct:>5.1f}% Processing: {filename}\033[0m")

        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(pdf_path)
        if not pdf_text:
            print(f"\033[91mFailed to extract text from {pdf_path}\033[0m")
            continue

        # Send the extracted text to ChatGPT for evaluation
        response = send_to_chatgpt(pdf_text)

        try:
            # Parse the response as JSON
            response_json = json.loads(response)
            results[filename] = response_json

            # Update aggregate results based on the JSON response
            for category, evaluations in response_json.items():
                for key, value in evaluations.items():
                    if value == "True":
                        aggregate_results[f'{key}_true'] += 1
                    elif value == "False":
                        aggregate_results[f'{key}_false'] += 1
                    elif value == "N/A":
                        aggregate_results[f'{key}_na'] += 1
                    aggregate_results[f'{key}_total'] += 1

        except json.JSONDecodeError as e:
            # Handle invalid JSON responses
            print(f"\033[91mError parsing JSON for {filename}: {e}\033[0m")
            results[filename] = {"error": "Invalid JSON response", "response": response}

    # Calculate percentages for aggregate results
    for key in questions_keys:
        true_count = aggregate_results[f'{key}_true']
        total = aggregate_results[f'{key}_total']
        aggregate_results[f'{key}_true_pct'] = (true_count / total) * 100 if total > 0 else 0.0
        aggregate_results[f'{key}_false_pct'] = 100 - aggregate_results[f'{key}_true_pct']

    # Save results to JSON files
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "results.json"), "w") as fid:
        json.dump(results, fid, indent=4)

    with open(os.path.join(output_folder, "aggregate_results.json"), "w") as fid:
        json.dump(aggregate_results, fid, indent=4)

    # Post-process the aggregate results for a human-readable summary
    postprocess_aggregate_results(output_folder, questions_keys)

def postprocess_aggregate_results(folder: str, questions_keys):
    """
    Post-process the aggregated results and save them to a text file.

    Args:
        folder (str): Path to the folder containing the aggregated results.
        questions_keys (list): List of question keys (e.g., ['A1', 'A2', 'B1']).

    Returns:
        None
    """
    with open(os.path.join(folder, "aggregate_results.json"), "r") as fid:
        raw_data = json.load(fid)

        # Prepare the table header for the summary file
        header = f"{'Question':<10} {'True':<6} {'False':<6} {'N/A':<6} {'Total':<6} {'% True':<8} {'% False':<8}"
        separator = "-" * len(header)
        lines = [header, separator]

        # Process each question key to create rows for the summary
        for key in questions_keys:
            true_count = raw_data[f'{key}_true']
            false_count = raw_data[f'{key}_false']
            na_count = raw_data[f'{key}_na']
            total = raw_data[f'{key}_total']
            true_pct = raw_data[f'{key}_true_pct']
            false_pct = raw_data[f'{key}_false_pct']
            row = f"{key:<10} {true_count:<6} {false_count:<6} {na_count:<6} {total:<6} {true_pct:<8.1f} {false_pct:<8.1f}"
            lines.append(row)

        # Write the summary to a text file
        with open(os.path.join(folder, "summary.txt"), "w") as text_file:
            text_file.write("\n".join(lines))
