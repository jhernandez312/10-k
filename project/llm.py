import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re
from bs4 import BeautifulSoup
from sec_api import ExtractorApi
import prompt

API_KEY = 'd5411dfe21d11a783929523ed5a96a284652fea9f9ff5d7d3b3d237789a8f83b'
extractorApi = ExtractorApi(API_KEY)

# load the .env file
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY'),
)

model = "gpt-3.5-turbo-0125"
temperature = 0.3
max_tokens = 500
company = ""


#read .txt files
def read_file(filepath):
    """ Reads the entire file content, handling files with null bytes. """
    if not os.path.exists(filepath):
        print("File does not exist:", filepath)
        return None
    try:
        with open(filepath, 'rb') as file:  # Open as binary to handle potential null bytes.
            content = file.read()
            content = content.replace(b'\x00', b'')  # Remove null bytes.
        return content.decode('utf-8', errors='ignore')  # Decode ignoring errors after cleaning.
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

"""
# helper function to pretty print long, single-line text to multi-line text
def pprint(text, line_length=100):
  words = text.split(' ')
  lines = []
  current_line = ''
  for word in words:
    if len(current_line + ' ' + word) <= line_length:
      current_line += ' ' + word
    else:
      lines.append(current_line.strip())
      current_line = word
  if current_line:
    lines.append(current_line.strip())
  print('\n'.join(lines))


# URL of Tesla's 10-K filing
filing_10_k_url = 'https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm'

# extract text section "Item 1 - Business" from 10-K
item_1_text = extractorApi.get_section(filing_10_k_url, '1', 'text')

print('Extracted Item 1 (Text)')
print('-----------------------')
pprint(item_1_text[0:1500])
print('... cut for brevity')
print('-----------------------')
"""

# Function to extract and save section from 10-K to JSON
def extract_and_save_section(url, item_number, section_title):
    # Extract the text section using the SEC API
    section_text = extractorApi.get_section(url, item_number, 'text')

    # Format the extracted text into a JSON structure
    data = {
        "title": section_title,
        "content": section_text
    }

    # Define the JSON file name
    json_file_path = f"{section_title.replace(' ', '_')}_section.json"

    # Save to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Section '{section_title}' extracted and saved to {json_file_path}")

# Example usage: Extract and save "Item 1A - Risk Factors" from Tesla's 10-K
filing_10_k_url = 'https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm'
extract_and_save_section(filing_10_k_url, '1A', 'Risk Factors')

"""
def extract_section(content, start_marker, end_marker=None):
    # Extracts a section between two markers.
    if content is None:
        print("No content provided to extract from.")
        return None
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Start marker not found:", start_marker)
        return None
    start_idx += len(start_marker)

    if end_marker:
        end_idx = content.find(end_marker, start_idx)
        if end_idx == -1:
            print("End marker not found:", end_marker)
            return None
    else:
        end_idx = len(content)

    return content[start_idx:end_idx].strip()

def extract_risk_factors(file_path):
    # Read the entire 10-K file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define regular expression patterns to find the Risk Factors section
    # Adjust patterns as necessary based on document formatting
    start_pattern = re.compile(r"Item\s1A\.\sRisk\sFactors", re.IGNORECASE)
    end_pattern = re.compile(r"Item\s1B\.\sUnresolved\sStaff\sComments", re.IGNORECASE)

    # Find the start and end of the Risk Factors section
    start_match = start_pattern.search(content)
    end_match = end_pattern.search(content)

    if start_match and end_match:
        # Extract the Risk Factors section
        risk_factors_section = content[start_match.end():end_match.start()]
        return risk_factors_section.strip()
    else:
        return "Risk Factors section not found."


def parse_html(html_content):
    # Parses HTML content and extracts relevant data using BeautifulSoup.
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.text if soup.title else 'No title found'
    headers = [h.text for h in soup.find_all(['h2', 'h3'])]
    return {
        'title': title,
        'headers': headers
    }
def print_html_structure(content):
    # Prints the structure of HTML to help diagnose parsing issues.
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())  # This will print the whole HTML content in a more readable form

# Call this function to see the HTML structure
# print_html_structure(content)

# Main execution block
filepath = "sec-edgar-filings\\GE\\10-K\\0001193125-11-047479\\full-submission.txt"  # Ensure this path is correct
content = read_file(filepath)
if content is not None:
    sec_header = extract_section(content, '<SEC-HEADER>', '</SEC-HEADER>')
    risk_factors = extract_risk_factors(filepath)
    if sec_header:
        print("SEC Header:", sec_header)
    else:
        print("Failed to extract SEC Header.")
    if risk_factors:
        print("Risk Factors Section Extracted Successfully")
else:
    print("Failed to read file or file is empty.")
"""

def truncate_json_text(file_path, max_lines=3):
    """ Truncates the 'content' field in a JSON file to a specified number of lines. """

    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Split the content into lines and truncate
    lines = data['content'].splitlines()
    if len(lines) > max_lines:
        truncated_content = '\n'.join(lines[:max_lines])
    else:
        truncated_content = '\n'.join(lines)

    # Update the content in the JSON data
    data['content'] = truncated_content

    # Save the truncated data back to the JSON file or you can choose to simply print it
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Content truncated to {max_lines} lines and saved back to {file_path}")

file_path = "Risk_Factors_section.json"
truncate_json_text(file_path, max_lines=20)

"""
#prompts
system_message = prompt.system_message
prompt = prompt.generate_prompt(risk_factors)

messages=[

    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt}
]


def get_summary():
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content

print(risk_factors)
#print_html_structure(content)
#print(content)
#print(get_summary())
"""