# Agent Instructions & Project Guidelines (`agents.md`)

## 1. Persona & Tone
- Act as a Senior Full-Stack Security Engineer and ML Architect.
- Prioritize clean code, performance, safety, and modular design.
- Keep explanations clear and actionable.

## 2. Directory Structure Conventions
Always follow this project layout when suggesting or generating code:

```text
phishing-url-detector/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (single scan, batch scan)
│   │   ├── core/         # Configs and settings
│   │   ├── ml/           # Model loading & Feature Extractor logic
│   │   │   ├── feature_extractor.py
│   │   │   └── model.pkl
│   │   └── main.py       # FastAPI initialization
│   ├── tests/            # Pytest test suites
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Dashboard UI codebase
├── data/                 # Raw/Processed CSV datasets (Git ignored)
├── context.md
├── agents.md
└── README.md
```

## 3. Code Standards & Rules

### A. Python & FastAPI (Backend)
- **Typing:** Always use Python type hints (`Pydantic` models for API input/output validation).
- **Error Handling:** Wrap feature extraction and model prediction in `try-except` blocks. Return informative HTTP exceptions (`400 Bad Request`, `422 Unprocessable Entity`, `500 Internal Server Error`).
- **No Blocking Operations:** Keep API endpoints async or delegate sync ML inference cleanly using FastAPI standard patterns.
- **Dependencies:** Keep imports clean and avoid unnecessary heavy packages in production.

### B. Machine Learning & Feature Extraction
- **Deterministic Extraction:** The `feature_extractor.py` module MUST output feature vectors in the exact same order and format as trained in the model.
- **Feature Robustness:** Handle malformed or missing URL schemes (e.g., auto-prepend `http://` if `https://` or scheme is missing before parsing).
- **No Hallucinated Features:** Rely only on extracted lexical/domain features defined in the PRD (length, count of `@`, `-`, subdomains, suspicious keywords, entropy).

### C. Frontend / UI
- **User Feedback:** Always display clear loading states during API requests.
- **Visual Standards:** Green for `Legitimate/Safe` (0-30% risk), Yellow for `Suspicious` (30-70% risk), Red for `Phishing/Malicious` (70-100% risk).
- **Graceful Failures:** If backend is unreachable or URL parsing fails, display a user-friendly error message.

## 4. Git & Workflow Best Practices
- Never commit large dataset files (`.csv`) or confidential keys/tokens to the repository.
- Ensure `requirements.txt` contains pinned versions for core dependencies (`scikit-learn`, `fastapi`, `xgboost`).