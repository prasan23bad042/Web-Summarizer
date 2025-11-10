# Real-Time Web Summarizer Extension with Qwen-Agent

Week 1 (Days 1–2): environment + scaffold.

## Quick Start

1. **Create `.env` from `.env.example`** and fill `DASHSCOPE_API_KEY` when ready.

2. **Create venv, install:**

   ```bash
   python -m venv .venv && source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. **Run backend (dev):**

   ```bash
   ./scripts/dev.sh
   ```

4. **Load the Chrome extension:**

   - Navigate to `chrome://extensions`
   - Enable "Developer Mode"
   - Click "Load unpacked"
   - Select the `extension/` folder

5. **Test:**
   - Visit a page → right-click → "Summarize Page"
   - Or open the popup and paste a URL or text

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── scripts/
│   ├── dev.sh
│   └── run.sh
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── routers/
│   │   │   └── summarize.py
│   │   └── services/
│   │       ├── fetch.py
│   │       └── summarize.py
│   └── tests/
│       └── test_health.py
└── extension/
    ├── manifest.json
    ├── background.js
    ├── content.js
    ├── popup.html
    ├── popup.js
    └── styles.css
```

## API Endpoints

- **GET** `/health` - Health check
- **POST** `/api/summarize` - Summarize URL or text
- **WebSocket** `/ws` - Real-time summarization

## Next Steps

1. Replace stub summarizer with Qwen-Agent pipeline using `DASHSCOPE_API_KEY` + `QWEN_MODEL`
2. Add streaming summaries over WebSocket
3. Improve content extraction and add caching/error handling
4. Add more tests

## Testing

```bash
# Run tests
python -m pytest -q

# Test health endpoint
curl http://127.0.0.1:8000/health

# Test summarize endpoint
curl -X POST http://127.0.0.1:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"FastAPI is a modern web framework."}'


EOF

echo ""
echo "✅ Project setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.example to .env and add your DASHSCOPE_API_KEY"
echo "2. Run tests: python -m pytest -q"
echo "3. Start dev server: ./scripts/dev.sh"
echo "4. Load Chrome extension from the extension/ folder"
echo ""
echo "🎉 Happy coding!"
```
