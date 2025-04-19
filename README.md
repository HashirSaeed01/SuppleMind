# 🧠 SuppleMind – Reddit-Powered Supplement Insight Engine

**SuppleMind** is a full-stack application that leverages Reddit data to extract and surface health & supplement-related insights. Users can query health conditions, vitamins, symptoms, or nootropics, and receive intelligent summaries based on real-time Reddit discussions.

Built using a React frontend and Flask backend, the app fetches subreddit data via Reddit’s API, processes the content, and stores it in **QuadrantDB** for fast and scalable access. Ideal for tracking supplement trends, understanding anecdotal experiences, and analyzing community sentiment around chronic issues like histamine intolerance, MCAS, and more.

---

## 🔍 Use Cases

- 🔎 Search how Redditors are reacting to supplements like **Magnesium Glycinate**, **SAM-e**, or **Vitamin B12**
- 📊 Discover common side-effects, dosage patterns, or timelines based on community responses
- 🤖 Query keywords and get summarized health trends and feedback sentiment

---

## ⚙️ Tech Stack

| Layer         | Tech                                     |
|---------------|------------------------------------------|
| Frontend      | React (Vite), TailwindCSS                |
| Backend       | Flask (Python), Reddit API (PRAW)        |
| DB Layer      | QuadrantDB (time-series optimized store) |
| NLP/Parsing   | spaCy, TextBlob (or custom)              |
| Deployment    | Docker, Render/Vercel/Fly.io             |

---

## 🧠 Architecture

```plaintext
User → React Frontend
           ↓
     Flask Backend
           ↓
  Reddit API Fetcher & Parser
           ↓
Keyword Extractor / Sentiment Engine
           ↓
       QuadrantDB
           ↑
   Smart Query Layer
           ↑
React UI displays insights

