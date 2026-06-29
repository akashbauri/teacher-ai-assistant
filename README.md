# 📚 NCF 2023 AI Teacher Assistant

An AI-powered Enterprise Knowledge Assistant for educators that transforms educational documents into classroom-ready teaching resources aligned with **NCF 2023** and **NEP 2020**.

The platform combines **Retrieval-Augmented Generation (RAG)**, **Semantic Search**, and **Large Language Models (LLMs)** to help teachers create high-quality educational content in seconds.

---

# 🚀 Project Overview

Teachers spend hours preparing lesson plans, notes, assessments, and classroom activities.

NCF 2023 AI Teacher Assistant reduces this effort by allowing teachers to upload educational documents and instantly generate:

* 📘 Study Notes
* 📋 Lesson Plans
* 👨‍🏫 Teaching Guides
* 📝 Question Papers
* ✅ MCQs
* 🎯 Learning Outcomes
* 🧠 Competencies
* 🗺️ Mind Maps
* 🔄 Flow Charts
* 📖 Chapter Summaries
* ❓ Important Questions

The system retrieves relevant information from uploaded documents using **Semantic Search** and generates context-aware educational content using **Groq LLM**.

---

# ✨ Current MVP Features

## 📄 Intelligent Document Processing

Supported Formats:

* PDF
* DOCX
* TXT

Capabilities:

* Text Extraction
* Smart Text Chunking
* Semantic Embeddings
* FAISS Vector Search
* Enterprise Metadata Generation

---

## 🤖 Enterprise RAG Pipeline

The application follows a Retrieval-Augmented Generation architecture.

Workflow:

Document Upload
↓
Text Extraction
↓
Smart Chunking
↓
Sentence Embeddings
↓
FAISS Vector Index
↓
Semantic Retrieval
↓
Groq LLM
↓
Classroom Ready Response

---

## 💬 AI Question Answering

Teachers can ask natural language questions directly from uploaded documents.

Features:

* Document-based Answers
* Context-aware Responses
* Semantic Retrieval
* Web Search Fallback
* Teacher-friendly Explanations
* Hallucination Reduction Prompting

---

# 📚 Classroom Resource Generation

## 📘 Study Notes

Automatically generates:

* Chapter Overview
* Learning Outcomes
* Competencies
* Key Concepts
* Detailed Notes
* Revision Notes
* Summary
* Real-life Examples

---

## ✅ Competency-Based MCQs

Supports multiple assessment styles:

* Single Correct Answer
* Multiple Correct Answers
* All of the Above
* None of the Above
* Assertion & Reason
* Case-Based Questions
* Activity-Based Questions
* Competency-Based Questions
* Real-Life Scenario Questions

---

## 📝 Question Paper Generator

Automatically creates:

* Easy Questions
* Moderate Questions
* Hard Questions
* Case-Based Questions
* Activity-Based Questions
* Competency Mapping
* Marks Distribution
* Answer Key

---

## 📋 Lesson Plan Generator

Generates complete classroom-ready lesson plans including:

* Curricular Goals
* Learning Outcomes
* Competency Mapping
* Teacher Script
* Student Activities
* Art Integrated Learning
* Game Based Learning
* Activity Based Learning
* Reflection Activities
* Assessment Rubrics
* Real-life Applications

---

## 👨‍🏫 Teaching Guide Generator

Includes:

* Teacher Instructions
* Student Responses
* Teaching Strategies
* Classroom Activities
* Misconceptions
* Assessments
* Homework
* Extension Activities

---

## 🗺️ Visual Learning Resources

### Flow Charts

Educational process flow including:

* Prior Knowledge
* Introduction
* Exploration
* Concept Building
* Activity
* Discussion
* Assessment
* Reflection

### Mind Maps

Automatically generates:

* Core Concepts
* Learning Outcomes
* Competencies
* Activities
* Assessment
* Real-life Applications

---

# 🎯 NCF 2023 & NEP 2020 Alignment

Current implementation supports:

* Competency-Based Learning
* Activity-Based Learning
* Inclusive Education
* Inquiry-Based Learning
* Critical Thinking
* Problem Solving
* Communication Skills
* Collaboration
* Creativity
* Art Integrated Learning
* Game Based Learning
* Real-life Applications

---

# 🏗️ Enterprise RAG Features

The platform includes enterprise-grade retrieval capabilities.

### Source Citation

Every AI response includes:

* Document Name
* Page Number
* Chunk Number
* Subject
* Chapter

---

### Retrieval Metadata

Displays:

* Similarity Score
* Confidence Score
* Retrieval Score
* Retrieval Rank
* Retrieval Method
* Generation Timestamp

---

### Explainable AI

The system provides transparent answers by exposing retrieval metadata alongside every generated response.

---

# 📊 Document Intelligence Dashboard

After uploading a document, the application displays:

* Document Name
* Word Count
* Character Count
* Indexed Chunks
* Embedding Model
* Vector Database
* System Status
* Response Time

---

# 📄 PDF Export

Generated resources can be exported as PDF.

Each exported document includes:

* Generated Content
* Source Information
* Retrieval Metadata
* Generation Timestamp

---

# ⚙️ Technology Stack

## Frontend

* Streamlit

## Large Language Model

* Groq API
* Llama 3.3 70B Versatile

## Vector Search

* FAISS

## Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

## Web Search

* Tavily Search

## PDF Generation

* ReportLab

---

# 🏛️ Current Architecture

User
↓
Streamlit UI
↓
Document Parser
↓
Chunk Generator
↓
Sentence Transformer
↓
FAISS Vector Index
↓
Semantic Retrieval
↓
Groq LLM
↓
Generated Educational Content

---

# 🚀 Future Roadmap

## Phase 2 — Enhanced Educational Intelligence

Planned additions:

* Complete NCF 2023 Knowledge Base
* Subject-wise Competency Mapping
* Curriculum Goal Alignment
* Panchpadi Learning Framework
* 5E Learning Model
* Bloom's Taxonomy Integration

Benefits:

* Better lesson planning
* Improved competency mapping
* Higher curriculum alignment

---

## Phase 3 — Enterprise AI Infrastructure

### Redis Cache

Purpose:

* Cache frequently generated responses

Benefits:

* Faster response times
* Reduced LLM API costs
* Better scalability
* Lower latency

---

### PostgreSQL / Supabase

Purpose:

* User Accounts
* Chat History
* Saved Resources
* Document Management
* Analytics

Benefits:

* Persistent storage
* Personalized teacher experience

---

### LangGraph

Purpose:

* Multi-step AI reasoning
* Educational workflow orchestration
* Intelligent planning

Benefits:

* Smarter lesson planning
* Better educational reasoning
* Agent-based workflows

---

### MCP (Model Context Protocol)

Purpose:

Connect external educational systems and tools.

Benefits:

* Curriculum APIs
* External knowledge integration
* Tool interoperability
* Future-ready architecture

---

## Phase 4 — Multi-Agent Teacher Ecosystem

Planned AI Agents:

* Curriculum Agent
* Lesson Planning Agent
* Assessment Agent
* Teaching Strategy Agent
* Inclusive Education Agent
* Classroom Activity Agent
* Student Performance Analysis Agent

---

# 📈 Expected Final Capabilities

The complete platform will provide:

* ✅ Enterprise Knowledge Assistant
* ✅ NCF 2023 Aligned Teaching Resources
* ✅ Competency-Based Assessments
* ✅ Curriculum Goal Mapping
* ✅ Panchpadi Learning Framework
* ✅ 5E Learning Framework
* ✅ Bloom's Taxonomy Integration
* ✅ Explainable AI Responses
* ✅ Multi-Agent Educational Intelligence
* ✅ Personalized Teacher Workspace
* ✅ Enterprise AI Infrastructure

---

# 🎯 Vision

Our vision is to build an **AI Teacher Copilot** that empowers educators with intelligent, explainable, and curriculum-aligned teaching assistance.

By combining **Enterprise RAG**, **Semantic Search**, **LLMs**, and future technologies such as **Redis**, **LangGraph**, **MCP**, and **PostgreSQL**, the platform aims to become a comprehensive educational assistant that significantly reduces teacher preparation time while improving classroom quality, engagement, and learning outcomes.

---

# 👨‍💻 Built With

* Streamlit
* Groq
* FAISS
* Sentence Transformers
* ReportLab
* Tavily Search
* NCF 2023
* NEP 2020

**Version:** 1.0 MVP
