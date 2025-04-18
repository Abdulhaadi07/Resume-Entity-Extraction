from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import json
from tika import parser
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai  # Gemini LLM integration

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'rtf', 'odt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Gemini API client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    """Extract text from various file formats using Apache Tika."""
    try:
        parsed = parser.from_file(file_path)
        if parsed and 'content' in parsed:
            return parsed['content'].strip()
        else:
            print(f"Tika parsing failed or returned no content for: {file_path}")
            return None
    except Exception as e:
        print(f"Error extracting text with Tika: {str(e)}")
        return None

def process_resume_with_llm(text):
    """Process resume text with Gemini API."""
    try:
        system_prompt = """
        You are an advanced resume parsing expert specializing in extracting and standardizing professional information. Your task is to comprehensively process the provided resume text with meticulous attention to detail:
        Parsing and Standardization Requirements:

        Abbreviation Normalization

        Convert all abbreviations to their full, standard forms
        Examples:

        "O.U." → "Osmania University"
        "B.Tech" → "Bachelor of Technology"
        "MS" → "Master of Science"

        Entity Consistency and Contextualization

        Align and standardize repeated entities across different sections
        Ensure consistent representation of:

        Company names
        Educational institutions
        Certifications
        Skill terminology
        Example: If "Google" appears in work experience, internships, and certifications, standardize its representation

        Structured Data Extraction
        Extract key resume entities into a comprehensive, well-structured JSON format
        Mandatory JSON fields should include:

        Personal Information
        Education
        Work Experience
        Skills
        Certifications
        Projects
        Achievements
        Data Quality Enhancements
        Resolve inconsistent naming conventions
        Expand industry-specific acronyms
        Normalize date formats
        Correct minor typographical errors

        Output Specifications
        Provide a clean, machine-readable JSON structure
        Ensure all extracted information is properly typed (strings, arrays, nested objects)
        Include confidence scores for extracted entities where applicable

        The goal is to transform raw resume text into a standardized, structured, and easily processable format that maintains the original information's integrity and context.
        """

        prompt = f"{system_prompt}\n\n{text}"

        response = model.generate_content(prompt)

        print("Raw Gemini API Response:", response.text)  # Debugging the response text

        content = response.text

        # Extract JSON from the Markdown code block
        json_start = content.find("```json")
        json_end = content.find("```", json_start + 1)

        if json_start != -1 and json_end != -1:
            json_string = content[json_start + 7 : json_end]  # Extract content between ```json and ```
            try:
                parsed_resume = json.loads(json_string)
                return parsed_resume
            except json.JSONDecodeError as json_err:
                print(f"Error decoding JSON: {json_err}")
                print(f"Problematic JSON string: {json_string}")
                return None
        else:
            print("Could not find JSON code block in Gemini API response.")
            return None

    except Exception as e:
        print(f"Error processing with Gemini API: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/parse', methods=['POST'])
def parse_resume():
    try:
        resume_text = None

        # Check if file is included in the request
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    file.save(temp_file.name)
                    resume_text = extract_text_from_file(temp_file.name)
                os.unlink(temp_file.name)
        # If file is not provided, use the manually entered text
        else:
            resume_text = request.form.get('resume_text')

        if not resume_text:
            return jsonify({'error': 'No resume content provided'}), 400

        # Process the resume content with Gemini LLM
        parsed_resume = process_resume_with_llm(resume_text)
        
        # If resume parsing is successful, return the parsed content
        if parsed_resume:
            return jsonify(parsed_resume)
        else:
            return jsonify({'error': 'Failed to parse resume'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/parse_resume', methods=['POST'])
def parse_resume_api():
    """API endpoint for parsing resumes from the frontend."""
    try:
        data = request.json
        resume_content = data.get('resume_content')

        if not resume_content:
            return jsonify({"error": "Resume content is required"}), 400

        parsed_resume = process_resume_with_llm(resume_content)

        if parsed_resume:
            return jsonify({"parsed_resume": parsed_resume})
        else:
            return jsonify({"error": "Failed to parse resume"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
