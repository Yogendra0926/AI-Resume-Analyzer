# 🤖 AI Resume Analyzer

An AI-powered Resume Analyzer that helps users understand and improve their resumes.

Users can upload their resume in PDF format and receive an intelligent analysis using AI.

## ✨ Features

- 📄 Upload Resume in PDF format
- 🤖 AI-powered Resume Analysis
- 💡 Identify Key Skills
- 💪 Analyze Resume Strengths
- ⚠️ Identify Weaknesses
- 🚀 Get Suggestions and Improvements
- 💼 Find Best Suitable Job Roles
- ⭐ Get a Resume Score out of 10
- 🎨 Modern and Responsive Streamlit UI

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Ollama
- Qwen3 4B
- PyPDFLoader
- Recursive Character Text Splitter

## ⚙️ How It Works

1. Upload your Resume PDF.
2. The application extracts text from the resume.
3. The resume text is split into manageable chunks.
4. The AI model analyzes the resume.
5. The application generates insights, suggestions, suitable job roles, and a resume score.

## 🚀 Run the Project

Install the required dependencies:

pip install streamlit langchain langchain-community langchain-text-splitters langchain-ollama pypdf

Download the Ollama model:

ollama pull qwen3:4b

Run the application:

streamlit run resumeapp.py

## 👨‍💻 Built With

Built using Streamlit and Ollama to explore the practical use of Generative AI in career and resume analysis.
