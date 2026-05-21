# Debatify

AI-powered parliamentary debate summarization and semantic retrieval system built using Ollama, FAISS, and Docling.

Debatify processes parliamentary debate PDFs, extracts structured text, generates concise summaries, creates semantic vector indexes, and enables intelligent querying over debate content using local LLMs.

---

## Features

- PDF parliamentary debate extraction
- AI-generated debate summaries
- Semantic search using FAISS
- Retrieval-Augmented Generation (RAG)
- Question-answering over debate documents
- Local LLM inference using Ollama
- Structured output generation
- Vector embedding storage
- Offline/local-first processing

---

## Tech Stack

### Backend
- Python

### AI / NLP
- Ollama
- FAISS
- Docling

### Additional Libraries
- Sentence Transformers
- PDF/Text Processing Utilities

---

## Project Structure

```bash
Debatify/
│
├── parliament-debate-summarizer/
│   ├── main.py
│   ├── chat.py
│   │
│   ├── extractor/
│   ├── summarizer/
│   ├── vector/
│   ├── src/
│   │
│   ├── input/
│   ├── outputs/
│   │
│   ├── vector.faiss
│   └── README.md
│
└── requirements.txt
```

---

## How It Works

1. Add parliamentary debate PDFs to the `input/` directory.
2. Extract text from debate documents.
3. Generate AI-powered summaries.
4. Create vector embeddings using FAISS.
5. Store processed outputs and vector indexes.
6. Query debates semantically using local LLMs through Ollama.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RanawatAnkit/Debatify.git
cd Debatify
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama from:

https://ollama.com

---

## Pull Required Model

Example:

```bash
ollama pull llama3
```

You can replace the model with any Ollama-supported local model.

---

## Usage

### Add Debate PDFs

Place debate PDF files inside:

```bash
input/
```

---

### Run Main Pipeline

```bash
python main.py
```

This will:
- extract text
- summarize debates
- generate embeddings
- create FAISS indexes
- store outputs

---

### Start Chat / Retrieval System

```bash
python chat.py
```

This enables semantic querying and AI-assisted retrieval over processed debate documents.

---

## Outputs

Generated outputs are stored inside:

```bash
outputs/
```

Possible outputs include:
- extracted text
- summaries
- metadata
- embeddings
- processed JSON data

---

## FAISS Vector Storage

Vector indexes are stored using FAISS for fast semantic similarity search.

Example generated files:

```bash
vector.faiss
```

---

## Use Cases

- Parliamentary debate analysis
- Legislative research
- Political summarization
- Semantic document retrieval
- Offline AI document assistant
- RAG experimentation using local LLMs

---

## Future Improvements

- Web dashboard
- Multi-document chat
- Speaker-wise analytics
- Topic clustering
- Debate sentiment analysis
- Streaming responses
- API support
- Docker deployment

---

## Requirements

- Python 3.10+
- Ollama
- FAISS-compatible environment

---


## License

This project is licensed under the MIT License.

---

## Author

Ankit Ranawat

GitHub:
https://github.com/RanawatAnkit

---

## Repository

https://github.com/RanawatAnkit/Debatify
