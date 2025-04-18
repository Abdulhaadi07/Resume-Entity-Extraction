# 🧠 Resume Parser with Google Gemini AI

This project is a web-based Resume Parser built with **Flask** and powered by **Google Gemini 1.5 Flash**. It extracts and structures information such as personal details, education, work experience, skills, projects, and more from a resume (PDF, DOCX, etc.).

---

## 🚀 Features

- Upload resumes or paste resume content manually  
- Parses resume content using **Textract** for text extraction  
- Uses **Gemini AI** to analyze and extract structured data  
- Outputs structured data in a clean **JSON format**  
- Simple and clean Flask web interface  

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **AI Model**: Google Gemini 1.5 Flash  
- **Text Extraction**: Textract  
- **Frontend**: HTML (Jinja Templates)  
- **Deployment**: Localhost (can be extended to any cloud platform)  

---

## 📦 Folder Structure

resume-parser-gemini/ │ 
├── uploads/ # Folder to hold uploaded resumes 
├── templates/ │ └── index.html # Web UI for resume upload and input 
├── .env # Store Gemini API Key securely 
├── app.py # Main application logic
├── requirements.txt # Project dependencies 
└── README.md # You're reading it!


---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-parser-gemini.git
cd resume-parser-gemini

### 2. Create & Activate Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add Your Gemini API Key

Create a `.env` file in the root folder and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

### ▶️ Run the App

```bash
python app.py
```

Then open your browser and go to:  
[http://localhost:5000](http://localhost:5000)

---

### 💡 Example Output

```json
{
  "personal_information": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "+1-555-987-6543",
    "linkedin": "linkedin.com/in/janedoe",
    "location": "New York, NY"
  },
  "education": [
    {
      "institution": "MIT",
      "degree": "Bachelor of Science",
      "major": "Computer Science",
      "graduation_date": "2023-05"
    }
  ],
  "experience": [
    {
      "company": "Google",
      "title": "Software Engineer",
      "start_date": "2023-07",
      "end_date": "Present"
    }
  ]
}
```

---

### 🧪 Sample Resumes for Testing

You can upload resumes in `.pdf`, `.docx`, or `.doc` format.

---

### ✨ To-Do

- [ ] Add downloadable JSON output  
- [ ] Improve input validation  
- [ ] Upload to cloud (Render, AWS, etc.)  
- [ ] Add authentication for multiple users  

---

### 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.
