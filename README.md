# 🏛️ Debatify — Parliament Debate Summarizer & Chat

**Turn hundreds of pages of Indian Parliament (Lok Sabha) debate PDFs into structured summaries you can search and chat with — fully offline, using local LLMs.**

Debatify reads an official Question Hour PDF (mixed Hindi + English), splits it into individual question–answer records, summarizes each one into clean structured JSON with **Llama 3 (via Ollama)**, indexes them in **FAISS**, and lets you ask natural-language questions about the day's debate through a **RAG (Retrieval-Augmented Generation)** chat.

> No paid APIs. No data leaves your machine.

---

## ✨ Features

- 📄 **Layout-aware PDF extraction** with [Docling](https://github.com/DS4SD/docling) (headings, lists, tables)
- ✂️ **Question segmentation** — multi-pattern regex detection + validation to isolate each Q&A, handling Hindi, English and legacy-font-encoded text
- 🧠 **Structured LLM summaries** — who asked, ministry, who answered, question summary, answer summary, overall summary, category
- 🌐 **Hindi → English** — summaries are always produced in simple, neutral English
- 🛡️ **Robust JSON pipeline** — two-stage prompting, balanced-brace JSON recovery, retries, schema validation
- ⏯️ **Resume support** — progress is saved after every question; interrupted runs continue where they stopped
- 🔎 **Semantic search** with Sentence-Transformers + FAISS
- 💬 **RAG chat** — ask questions in plain English and get answers grounded in the debate records
- 📁 **Per-date knowledge bases** — every debate date gets its own output folder

---

## 🏗️ Architecture

```
                 ┌──────────────── PIPELINE  (python main.py) ────────────────┐
  Debate PDF ──► 1. EXTRACT    Docling → extracted_text.txt
                 2. SPLIT      Regex markers + validator → questions.txt
                 3. SUMMARIZE  Llama 3 8B (Ollama), 2-stage prompt → final_summary.json
                 4. INDEX      all-MiniLM-L6-v2 embeddings → FAISS index + metadata.pkl
                 └────────────────────────────────────────────────────────────┘

                 ┌──────────────── CHAT  (python chat.py) ────────────────────┐
  Your question ──► embed ──► FAISS top-8 search ──► summaries as context
                ──► Llama 3 ──► grounded natural-language answer
                 └────────────────────────────────────────────────────────────┘
```

### How each stage works

| Stage | Module | What happens |
|---|---|---|
| **Extract** | `extractor/extractor.py` | Docling converts the PDF to structured text, saved for traceability. |
| **Split** | `extractor/extractor.py` | Four regex patterns find question starts (numbered MP names, `QUESTION n` headers, Hindi `क्या`, honorifics like SHRI/DR./SMT.). Blocks expand upward to capture headings, then a validator keeps real questions ("Will the Minister… be pleased to state") and drops annexure tables (`STATEMENT`, `State/UT-wise`). |
| **Summarize** | `summarizer/summarizer.py` | Text is cleaned (tables & procedural noise removed) and *smart-trimmed* (keeps the first 60% / last 40% of long blocks to fit the context window). **Stage 1** prompt produces a labelled factual summary; **Stage 2** prompt converts it to strict JSON. Malformed JSON is recovered or retried. Low temperature (0.1) + repeat penalty keep output factual. |
| **Index** | `vector/indexing.py` | Each summary (one per question) is embedded with `all-MiniLM-L6-v2` and stored in a FAISS `IndexFlatL2`; full records go into `metadata.pkl`. |
| **Chat** | `chat.py`, `src/` | The query is embedded, the top-8 most similar summaries are retrieved, and Llama 3 answers using only that context. |

### Sample output record

```json
{
  "id": 1,
  "language": "mixed",
  "has_table": false,
  "word_count": 484,
  "summary": {
    "asked_by": "Imran Masood",
    "ministry": "Rural Development and Panchayati Raj Ministry",
    "question_summary": "The MP asks about the measures taken by the government to address ...",
    "answered_by": "Minister of State for Rural Development and Panchayati Raj",
    "answer_summary": "The Minister responds that the government has taken several initiatives ...",
    "overall_summary": "...",
    "category": "Agriculture"
  }
}
```

### Results

| Debate date | Questions extracted | Structured summaries |
|---|---|---|
| 21 Jul 2025 | 175 | 174 |
| 22 Jul 2025 | 185 | 181 |

---

## 🧰 Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3.10+ |
| PDF parsing | Docling |
| Text segmentation | Python `re` (regex) |
| LLM | Llama 3 8B via [Ollama](https://ollama.com) (REST API) |
| Embeddings | Sentence-Transformers `all-MiniLM-L6-v2` |
| Vector store | FAISS (`faiss-cpu`) |
| Storage | JSON, Pickle |

---

## 📂 Project Structure

```
Debatify/
├── main.py                  # Runs the full pipeline: extract → summarize → index
├── chat.py                  # Interactive RAG chat over a processed debate date
├── requirements.txt
│
├── extractor/
│   └── extractor.py         # Docling PDF extraction + question splitting/validation
├── summarizer/
│   └── summarizer.py        # Ollama summarization, JSON cleaning, retries, resume
├── vector/
│   └── indexing.py          # Embeddings + FAISS index building
├── src/
│   ├── config.py            # Model names, Ollama URL, TOP_K
│   ├── retriever.py         # Index loading + similarity search
│   └── llm.py               # RAG answer generation prompt
│
├── input/                   # Put debate PDFs here
├── outputs/<date>/          # Generated per-date results (git-ignored)
└── sample input output/     # Example PDF and its generated outputs (21 Jul 2025)
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- ~8 GB RAM minimum (a GPU makes summarization much faster)

### 2. Clone & install

```bash
git clone https://github.com/RanawatAnkit/Debatify.git
cd Debatify

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Pull the LLM

```bash
ollama pull llama3:8b
```

Ollama must be reachable at `http://localhost:11434` (the default). To use a different model, edit `OLLAMA_MODEL` in `src/config.py` and `MODEL` in `summarizer/summarizer.py`.

### 4. Process a debate PDF

```bash
python main.py
```

You will be prompted for:

```
Enter PDF path: input/Monday, July 21, 2025.pdf
Enter debate date (example 21-07-2025): 21-07-2025
```

Outputs are written to `outputs/<date>/`:

| File | Contents |
|---|---|
| `extracted_text.txt` | Full text extracted from the PDF |
| `questions.txt` | One block per detected question & answer |
| `final_summary.json` | Structured summary for every question |
| `vector.*` / `metadata.pkl` | FAISS index and matching records |

> ⏱️ Summarization runs one LLM call pair per question and can take a while. If it's interrupted, just run it again — it resumes from the last saved question.

### 5. Chat with the debate

```bash
python chat.py
```

```
🏛 Parliament Debate Chat Ready
Enter debate date (example 21-07-2025): 21-07-2025
Ask: What did the government say about support for farmers returning to agriculture?
```

---

## ⚙️ Configuration (`src/config.py`)

| Setting | Default | Purpose |
|---|---|---|
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Sentence-Transformers embedding model |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama endpoint |
| `OLLAMA_MODEL` | `llama3:8b` | Model used for chat answers |
| `TOP_K` | `8` | Number of summaries retrieved per query |

---

## 🧩 Challenges Solved

- **Legacy Hindi font encoding** — the PDFs use non-Unicode fonts (e.g. `क्या` appears as `³या`), so detection patterns cover both forms.
- **No clean question boundaries** — solved with multiple start-marker patterns, upward context expansion and a good/bad-sign validator.
- **Small-model unreliability** — two-stage prompting, JSON recovery, strict retries, low temperature and stop tokens.
- **Long answers with large tables** — table stripping and head/tail smart trimming to fit an 8K context.
- **Hours-long runs** — checkpointing after every question with automatic resume.

---

## 🛣️ Roadmap

- [ ] REST API (FastAPI) and a web dashboard
- [ ] Cross-date search with metadata filters (date, ministry, MP, category)
- [ ] Normalized category taxonomy
- [ ] Cosine-similarity search (normalized embeddings) and multilingual embeddings for Hindi queries
- [ ] Source citations (question IDs) in chat answers
- [ ] Unicode repair for legacy-font Hindi text
- [ ] Speaker-wise analytics, topic clustering and Docker deployment

---

## 🎯 Use Cases

- Citizens and students understanding what was discussed in Parliament
- Journalists and researchers quickly finding ministry responses
- Policy analysis and legislative research
- A reference implementation of an offline, local-LLM RAG pipeline

---

## 📜 License

This project is licensed under the MIT License.

## 👤 Author

**Ankit Ranawat** — [github.com/RanawatAnkit](https://github.com/RanawatAnkit)
