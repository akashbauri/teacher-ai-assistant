# 📚 AI Teacher Assistant

## Overview

AI Teacher Assistant is an intelligent educational platform that helps teachers transform uploaded documents into teaching materials instantly.

Teachers can upload educational documents and:

* Ask questions about the content
* Generate notes
* Generate MCQs
* Generate question papers
* Create lesson plans
* Generate teaching guides
* Download outputs as PDF
* Get answers with source tracking

The platform explains concepts in a simple way, suitable for Class 5 students by default.

---

# 🎯 Problem Statement

Teachers spend significant time preparing:

* Notes
* Question papers
* MCQs
* Lesson plans
* Teaching strategies

This project automates these tasks using AI.

---

# 🚀 Features

## 1. Document Upload

Supported Formats:

* PDF
* DOCX
* TXT

Upload educational documents and let AI analyze the content.

---

## 2. Document Question Answering

Ask questions directly from uploaded documents.

Example:

What is Photosynthesis?

AI retrieves relevant content from the uploaded document and generates an answer.

---

## 3. Web Search Fallback

If the answer is not found in the uploaded document:

Question
↓
Web Search
↓
AI Answer

Source is displayed accordingly.

---

## 4. Notes Generator

Generate:

* Topic-wise Notes
* Revision Notes
* Summary Notes
* Important Points

---

## 5. MCQ Generator

Generate:

* Easy MCQs
* Moderate MCQs
* Hard MCQs
* Mixed MCQs

Each MCQ includes:

* Question
* 4 Options
* Correct Answer

---

## 6. Question Paper Generator

Generate question papers based on:

* 20 Marks
* 30 Marks
* 50 Marks

Difficulty Levels:

* Easy
* Moderate
* Hard
* Mixed

---

## 7. Lesson Plan Generator

Generate:

* Learning Objectives
* Introduction
* Activities
* Assessment
* Homework
* Recap

---

## 8. Teaching Guide Generator

Provides teachers with:

* Teaching Approach
* Classroom Activities
* Real-life Examples
* Student Engagement Tips
* Common Doubts
* Homework Suggestions

---

## 9. PDF Download

Generated outputs can be downloaded as PDF.

Supported:

* Notes
* MCQs
* Question Papers
* Lesson Plans
* Teaching Guides

---

## 10. Source Tracking

Every response displays the source.

Examples:

Source:
Uploaded Document

or

Source:
Web Search

---

# 🧠 AI Workflow

Upload Document
↓
Extract Text
↓
Chunk Text
↓
Create Embeddings
↓
Store in ChromaDB
↓
Teacher Question
↓
Semantic Search
↓
Retrieve Context
↓
OpenRouter LLM
↓
Generate Answer
↓
Show Source
↓
Download PDF

---

# 🏗 Architecture

Teacher
↓
Streamlit UI
↓
Document Parser
↓
ChromaDB
↓
RAG Engine
↓
OpenRouter
↓
PDF Generator

---

# 📂 Project Structure

teacher-ai-assistant/

app.py

requirements.txt

prompts.py

generators.py

pdf_generator.py

utils.py

document_parser.py

chroma_manager.py

rag_engine.py

.streamlit/
└── secrets.toml

README.md

---

# ⚙️ Technologies Used

Frontend:

* Streamlit

LLM:

* OpenRouter
* DeepSeek

Vector Database:

* ChromaDB

Embeddings:

* BAAI/bge-small-en-v1.5

Document Processing:

* PyPDF
* python-docx

Web Search:

* Tavily

PDF Generation:

* ReportLab

AI Framework:

* LangChain
* LangGraph (Future Upgrade)

---

# 🔑 Environment Variables

Create Streamlit Secrets:

OPENROUTER_API_KEY

TAVILY_API_KEY

Example:

OPENROUTER_API_KEY="your_key"

TAVILY_API_KEY="your_key"

---

# ▶️ Deployment

GitHub
↓
Streamlit Community Cloud
↓
Live Website

---

# 👨‍🏫 Example Use Cases

Example 1:

Upload Science Chapter

Ask:

Explain Photosynthesis

Result:

AI explains using document content.

---

Example 2:

Generate Easy MCQs

Result:

AI creates topic-based MCQs.

---

Example 3:

Generate 50 Marks Question Paper

Result:

AI generates a complete exam paper.

---

Example 4:

Create Lesson Plan

Result:

AI generates a classroom-ready teaching plan.

---

# 🔮 Future Enhancements

* LangGraph Agent
* MCP Architecture
* PostgreSQL Database
* Multi-document Search
* OCR Support
* Multi-language Support
* Student Dashboard
* School Dashboard
* Bloom's Taxonomy Integration

---

# 👤 Author

Akash Bauri

Founder – APPNA BANK

AI Freelancer

* Invisible Technologies
* Outlier AI

Passionate about AI, Automation, Education Technology, and Intelligent Learning Systems.

---

# 📜 License

This project is intended for educational and research purposes.
