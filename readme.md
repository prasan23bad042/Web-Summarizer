# Web Summarizer API 🌐  
### FastAPI | LLM (Qwen) | Async Web Processing

Web Summarizer is a **FastAPI-based backend service** that generates concise summaries from **web pages or raw text** using a large language model (Qwen via DashScope).  
It supports both **REST APIs** and **WebSocket-based real-time summarization**.

---

## 📌 Overview

This project provides an API that:
- Accepts a **URL or plain text**
- Fetches and cleans web content (if URL is provided)
- Generates a concise summary using an **LLM**
- Returns the summary via HTTP or WebSocket

It is designed to demonstrate:
- Asynchronous APIs
- LLM integration
- Web scraping and content extraction
- Rate limiting and caching
- Clean backend architecture

---

## 🚀 Features

- 🔗 Summarize content directly from a **URL**
- 📝 Summarize **raw text input**
- ⚡ Asynchronous processing using FastAPI
- 🧠 LLM-powered summarization (Qwen / DashScope)
- 🔄 WebSocket support for real-time summaries
- 🧹 Automatic webpage content extraction & cleanup
- 🛑 Rate limiting to prevent abuse
- 🧠 In-memory caching for faster repeated requests
- 🌍 CORS enabled for frontend integration
- ❤️ Health check endpoint

---

## 🧑‍💻 Tech Stack

- **Python 3.9+**
- **FastAPI**
- **Pydantic**
- **HTTPX**
- **BeautifulSoup**
- **DashScope (Qwen LLM)**
- **WebSockets**
- **Async / Await**

---

## 🧠 How It Works

1. Client sends a request (URL or text)
2. If URL:
   - Webpage is fetched asynchronously
   - HTML is cleaned (scripts, styles, headers removed)
3. Clean text is sent to the Qwen LLM
4. Summary is generated based on max length
5. Result is returned to the client
6. Summary may be cached for future requests

---

## 📡 API Endpoints

### 🔹 POST `/api/summarize`

Generate a summary from a URL or text.

**Request Body**
```json
{
  "type": "url",
  "content": "https://example.com/article",
  "max_length": 300
}
