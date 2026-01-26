# Fact-Checking Web App (App Link-https://fact-checker-app-ewdwddu7ddqx4vqbpb6xpk.streamlit.app/)

## Overview
This project is a deployed web application that automates factual claim verification from PDF documents.  
It is designed to act as a “fact-checking layer” between content drafts and publication.

The app ingests a PDF report, extracts factual claims (statistics, dates, financial figures, and concrete assertions), verifies those claims against **live web data**, and flags each claim as **Verified**, **Inaccurate**, or **False**.

---

## How It Works

The system operates in three main stages:

### 1. PDF Ingestion & Text Extraction
- Users upload a PDF via the web interface.
- The app uses `pypdf` to extract raw text from each page of the document.
- The extracted text is passed downstream for analysis.

### 2. Claim Extraction (LLM-powered)
- The extracted text is sent to Gorq via LangChain.
- A structured prompt instructs the model to extract **only checkable factual claims**, such as:
  - Numerical statistics
  - Dates and timelines
  - Financial figures
  - Technical or market assertions
- The output is a clean list of individual claims.

### 3. Live Verification via Web Search
- Each claim is queried against the live web using Tavily Search.
- Relevant sources and snippets are retrieved in real time.
- Claims are classified as:
  - **Verified** – supported by current, credible sources
  - **Inaccurate** – partially correct or outdated information
  - **False** – no credible evidence found

Supporting evidence is displayed alongside each claim for transparency.

---

## User Interface
- Built with **Streamlit**
- Simple drag-and-drop PDF upload
- Clear, readable results with visual status indicators
- No local installation required for end users

---

## Tech Stack

- **Frontend / App Framework:** Streamlit  
- **Backend / Logic:** Python  
- **LLM Orchestration:** LangChain  
- **Language Model:** OpenAI GPT-4o  
- **Web Search:** Tavily API  
- **PDF Parsing:** pypdf  

---

## Deployment
- The app is deployed on **Streamlit Cloud**
- Environment variables (`OPENAI_API_KEY`, `TAVILY_API_KEY`) are securely configured in Streamlit Cloud settings
- No API keys are stored in the repository

---

## Repository Structure

fact-checker-app/
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── services/
    ├── pdf_loader.py # PDF text extraction
    ├── claim_extractor.py # LLM-based claim extraction
    ├── web_search.py # Live web search logic
    └── verifier.py # Claim verification and classification


---

## Evaluation Alignment
This app is designed to correctly flag:
- Intentional falsehoods
- Widely circulated myths
- Outdated or incorrect statistics

It prioritizes **accuracy, live data verification, and transparency**, aligning directly with the assessment criteria.

---





