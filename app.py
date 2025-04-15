import streamlit as st
import google.generativeai as genai
import os
import pdfplumber
from dotenv import load_dotenv
import json
import re

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel('models/gemini-2.0-pro-exp')
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return ""

def input_pdf_text(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def clean_json_response(response):
    try:
        response = response.strip()
        response = re.sub(r'```json|```', '', response)
        response = re.sub(r'\s+', ' ', response)
        response = response.replace("\n", '').replace("\r", '')
        response = response.replace('”', '"').replace('“', '"')
        response = response.replace('’', "'").replace('‘', "'")
        return response
    except Exception as e:
        st.error(f"Error cleaning response: {e}")
        return response

def normalize_keys(data):
    return {key.replace(' ', '').replace('"', ''): value for key, value in data.items()}

input_prompt = """
Hey, act like a highly experienced ATS (Applicant Tracking System) with expertise in tech fields. 
Your job is to evaluate the resume against the provided job description.

Ensure the response is returned in valid JSON format:
{"OverallATSScore":"%","JDMatch":"%","MissingKeywords":[],"SkillGaps":[],"ProfileSummary":""}

resume:{text}
description:{jd}
"""

st.title("Smart ATS")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        if text:
            prompt = input_prompt.format(text=text, jd=jd)
            response = get_gemini_response(prompt)
            if response:
                try:
                    cleaned_response = clean_json_response(response)
                    st.text_area("Debug Raw Response", cleaned_response)  # Debugging step
                    parsed_response = json.loads(cleaned_response)
                    parsed_response = normalize_keys(parsed_response)
                    
                    overall_score = parsed_response.get('OverallATSScore', 'N/A')
                    jd_match = parsed_response.get('JDMatch', 'N/A')
                    missing_keywords = parsed_response.get('MissingKeywords', [])
                    skill_gaps = parsed_response.get('SkillGaps', [])
                    profile_summary = parsed_response.get('ProfileSummary', 'N/A')
                    
                    st.markdown("## 📊 **Overall ATS Score:**")
                    st.markdown(f"<div style='font-size: 28px; font-weight: bold; color: #4CAF50;'>{overall_score}</div>", unsafe_allow_html=True)
                    
                    st.markdown("## 🟨 **JD Match:**")
                    st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #FF9800;'>{jd_match}</div>", unsafe_allow_html=True)
                    
                    st.markdown("## 🟥 **Missing Keywords:**")
                    missing_keywords_text = "<br>".join([f"<b style='font-size: 18px; color: #D32F2F;'>{kw}</b>" for kw in missing_keywords]) or "None"
                    st.markdown(f"<div style='background-color: #FFEBEE;'>{missing_keywords_text}</div>", unsafe_allow_html=True)
                    
                    st.markdown("## 🟠 **Skill Gaps:**")
                    skill_gaps_text = "<br>".join([f"<b style='font-size: 18px; color: #E65100;'>{gap}</b>" for gap in skill_gaps]) or "None"
                    st.markdown(f"<div style='background-color: #FFF3E0;'>{skill_gaps_text}</div>", unsafe_allow_html=True)
                    
                    st.markdown("## 🟦 **Profile Summary:**")
                    st.markdown(f"<div style='background-color: #FFCCCB;'>{profile_summary}</div>", unsafe_allow_html=True)
                    
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {e}")
                    st.text_area("Debug JSON Output", cleaned_response)
        else:
            st.warning("Could not extract text from the PDF. Please try another file.")
    else:
        st.warning("Please upload a resume to proceed.")
