from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import json
import openai
from tika import parser
import tempfile

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'rtf', 'odt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    """Extract text from various file formats using Apache Tika with explicit UTF-8 decoding."""
    try:
        parsed = parser.from_file(file_path)
        if parsed and 'content' in parsed:
            # Attempt to decode as UTF-8, which is a common and robust encoding
            try:
                return parsed['content'].strip()
            except UnicodeDecodeError as e:
                print(f"Error decoding Tika output with UTF-8: {e}")
                # Fallback to 'latin-1' which can handle a broader range of single-byte characters
                try:
                    return parsed['content'].encode('latin-1', errors='ignore').decode('latin-1')
                except Exception as fallback_e:
                    print(f"Error with fallback decoding: {fallback_e}")
                    return None  # Indicate failure to extract text
        else:
            print(f"Tika parsing failed or returned no content for: {file_path}")
            return None
    except Exception as e:
        print(f"Error extracting text with Tika: {str(e)}")
        return None

def process_resume_with_llm(text):
    """Process resume text with DeepSeek LLM."""
    try:
        load_dotenv()
        openai.api_key = os.getenv("DEEPSEEK_API_KEY")
        openai.api_base = "https://api.deepseek.com"
        system_prompt = """
        You are a resume parsing expert. Analyze the provided resume and:
         I need to perform the following tasks upon this :- Perform Resume parsing on this text. Make sure of these things --> 1)If if any words in the resume content are not normalized/standardized (for example are in abbreviation or short form or misspelt) they must be set to their standardized form. May be a word is an abbreviation--O.U. which has to be Osmania University, so if it's in abbreviation, standardize it in full form. Also there might be some words that may be used at multiple lines, (for example 'Google' may be used in multiple lines, as a Certification and Internship) the context of usage must be analyzed and aligned accordingly. In the end, the expected output is a parsed format of the resume. Provide me with that JSON Output.
         Make sure you remember to evaluate all the words that are in their short form or abbreviation so that in the output, their standardized format i.e. their full form is returned
        """

        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            stream=False
        )

        parsed_resume = json.loads(response.choices[0].message.content)
        return parsed_resume
    except Exception as e:
        print(f"Error processing with LLM: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_resume():
    try:
        resume_text = None

        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    file.save(temp_file.name)
                    resume_text = extract_text_from_file(temp_file.name)
                os.unlink(temp_file.name)
        else:
            resume_text = request.form.get('resume_text')

        if not resume_text:
            return jsonify({'error': 'No resume content provided'}), 400

        parsed_resume = process_resume_with_llm(resume_text)
        if parsed_resume:
            return jsonify(parsed_resume)
        else:
            return jsonify({'error': 'Failed to parse resume'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)