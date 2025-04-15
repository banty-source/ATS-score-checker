# ATS-score-checker

# ATS Score Checker

🚀 A smart AI-powered resume analyzer that evaluates your resume against a job description using Google's Gemini model.

## 🔍 Features

- 📄 Upload your resume in PDF format
- 📋 Paste any job description
- 🤖 Uses Gemini Pro to analyze content
- 📊 Outputs:
  - Overall ATS Score
  - JD Match Percentage
  - Missing Keywords
  - Skill Gaps
  - Profile Summary

## 🧠 Powered By

- **Google Generative AI (Gemini)**
- **Streamlit** for web interface
- **pdfplumber** for PDF text extraction

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/banty-source/ATS-score-checker.git
cd ATS-score-checker
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file with your Gemini API key:

ini
Copy
Edit
GOOGLE_API_KEY=your-api-key-here
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📎 Example Output

🛠️ Tech Stack
Python

Streamlit

Google Generative AI (Gemini)

pdfplumber

dotenv

📬 Contact
For issues or feature requests, open a GitHub issue or contact banty-source.
