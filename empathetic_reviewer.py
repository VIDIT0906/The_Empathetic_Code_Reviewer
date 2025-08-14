import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from a .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please create a .env file and set the GOOGLE_API_KEY variable.")
genai.configure(api_key=API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

# --- Prompt Engineering ---
def create_prompt(code_snippet, comments):
    """
    Creates a detailed, structured prompt for the Generative AI model.
    This prompt is engineered to meet all hackathon requirements, including the "Stand Out" features.
    """
    
    # Joining the list of comments into a single string for the prompt
    comments_str = "\n".join(f"- {comment}" for comment in comments)
    
    # The prompt is structured to guide the AI's response format and tone.
    prompt = f"""
        **Persona:** You are an expert senior software engineer and a patient, empathetic mentor. Your goal is to provide code review feedback that is constructive, educational, and encouraging, never discouraging.

        **Context:** I have a Python code snippet and a list of direct, critical review comments. I need you to transform this raw feedback into a supportive and educational report.

        **Code Snippet:**
        ```python
        {code_snippet}
        ```

        **Original Critical Comments:**
        {comments_str}

        **Your Task:**
        Generate a single, well-formatted Markdown report. For each original comment, create a separate section. Each section must contain exactly these three sub-headings:
        1.  ***Positive Rephrasing:*** A gentle and encouraging version of the feedback.
        2.  ***The 'Why':*** A clear, concise explanation of the underlying software engineering principle (e.g., performance, readability, best practices).
        3.  ***Suggested Improvement:*** A concrete, corrected code example demonstrating the recommended fix.

        **Stand Out Features (Please Implement):**
        - **Link to Resources:** Where applicable, include a markdown-formatted link to authoritative external documentation (like a specific Python PEP 8 rule or a relevant article) to support your suggestion.
        - **Holistic Summary:** After analyzing all individual comments, please add a final section titled "### Overall Feedback" that summarizes the review in an encouraging way, focusing on the learning opportunity.

        Begin the report immediately with the analysis of the first comment.
    """
    return prompt

# --- Main Execution Logic ---
def generate_empathetic_review():
    """
    Loads input, generates the review, and prints the output.
    """
    try:
        # Load input data from the JSON file
        with open('input.json', 'r') as f:
            input_data = json.load(f)
        
        code_snippet = input_data["code_snippet"]
        review_comments = input_data["review_comments"]

        # Create the prompt
        prompt = create_prompt(code_snippet, review_comments)

        # Initialize the Generative AI model and generate content
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        # Output the report
        print("--- Empathetic Code Review Report ---")
        print(response.text)

        # Save the report to a file for easy access
        with open('report.md', 'w') as f:
            f.write(response.text)
        print("\n--- Report also saved to report.md ---")

    except FileNotFoundError:
        print("Error: 'input.json' not found. Please make sure the file exists in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_empathetic_review()