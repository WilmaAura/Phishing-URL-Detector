# Product Requirements Document (PRD)
## Project Name: Phishing & Malicious URL Detector (ML-Powered Security Dashboard)

---

## 1. Executive Summary
The **Phishing & Malicious URL Detector** is a full-stack cybersecurity application powered by Machine Learning. The application evaluates given URLs (or domain names) in real-time, extracts lexical and domain features, and predicts whether the URL is **Legitimate**, **Phishing**, or **Malicious**. It includes an interactive Web UI for single URL analysis, CSV batch processing, and detailed risk breakdowns.

---

## 2. System Architecture & Flow

### High-Level Workflow
```
[User / Web Frontend]
       │
       ▼ (HTTP POST /api/v1/scan)
[FastAPI Backend Engine]
       │
       ├─► 1. Lexical Feature Extractor (URL length, special chars, IP usage, entropy)
       ├─► 2. Domain / Network Resolver (WHOIS age, DNS records, SSL cert check - optional)
       │
       ▼
[Trained Machine Learning Model (.pkl / .onnx)]
       │
       ▼ (Inference & Prediction Output)
[FastAPI Backend]
       │
       ▼ (JSON Response: Score, Label, Risk Factors)
[User / Web Frontend]
```

---

## 3. Recommended Datasets

For training the Machine Learning model, a hybrid dataset containing both legitimate and malicious/phishing URLs is required.

### 3.1 Primary Datasets
1. **PhishTank Database** (Active Phishing URLs)
   * **Source:** [PhishTank Data](https://www.phishtank.com/)
   * **Type:** Real-time verified phishing URLs (CSV/JSON format).
2. **Kaggle Malicious and Benign URLs Dataset**
   * **Source:** [Kaggle - Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) (~650,000 URLs).
   * **Types Included:** Benign, Definement, Malware, Phishing.
3. **Tranco / Majestic Million Top Websites** (Benign Baseline)
   * **Source:** [Tranco List](https://tranco-list.eu/)
   * **Type:** Top 1M legitimate global domains to balance class distribution.

### 3.2 Dataset Requirements
* **Target Size:** ~50,000 to 100,000 balanced samples (50% Legitimate, 50% Phishing/Malicious) for rapid training without high RAM usage.
* **Format:** CSV with two primary columns: `url` and `label` (0 for Legitimate, 1 for Phishing).

---

## 4. Tech Stack Specification

| Layer | Recommended Technology | Justification |
| :--- | :--- | :--- |
| **Machine Learning** | Python, `scikit-learn`, `XGBoost`, `pandas`, `joblib` | Fast training and easy serialization for backend production loading. |
| **Backend API** | Python (`FastAPI`), `pydantic`, `uvicorn` | Extremely lightweight, fast asynchronous execution, auto-generated OpenAPI docs. |
| **Frontend UI** | React / Next.js or HTML5 + Tailwind CSS + Vanilla JS | Responsive, modern dashboard UI with real-time risk gauges and tables. |
| **Deployment / Hosting** | Render / Railway / Hugging Face Spaces | Free-tier support for hosting FastAPI backend + React/Static frontend. |

---

## 5. Machine Learning Pipeline & Feature Engineering

### 5.1 Extracted Features (Feature Vector)
Instead of feeding raw text directly to complex NLP models, lexical and structural features are extracted from the URL for fast inference speed (<100ms):

1. **Length-Based Features:**
   * `url_length`: Total character count of the URL.
   * `hostname_length`: Length of the domain/hostname part.
   * `path_length`: Length of the path component.
2. **Character & Structural Counts:**
   * Counts of `@`, `?`, `-`, `=`, `.`, `%`, `http/https`, `//`.
   * Presence of IP address instead of domain name (e.g., `http://192.168.1.1/login`).
   * Count of subdomains (e.g., `login.paypal.verify.com` -> 3).
   * URL Entropy (measurement of randomness in character distribution).
3. **Keyword & Heuristic Signals:**
   * Count of suspicious keywords in path (`login`, `verify`, `bank`, `update`, `secure`, `account`).
   * Shortening service detection (e.g., `bit.ly`, `tinyurl.com`, `t.co`).
   * HTTPS presence and placement.

### 5.2 Model Selection
* **Primary Model:** **XGBoost Classifier** or **Random Forest Classifier**.
* **Target Metric:** **F1-Score >= 95%** and low False Positive Rate (minimizing flagging legitimate sites as phishing).

---

## 6. Functional Requirements

### 6.1 Backend API Specs

#### Endpoint 1: Analyze Single URL
* **Route:** `POST /api/v1/analyze`
* **Request Body:**
  ```json
  {
    "url": "http://paypal-security-update.com/login.php"
  }
  ```
* **Response Body:**
  ```json
  {
    "url": "http://paypal-security-update.com/login.php",
    "prediction": "Phishing",
    "risk_score": 0.94,
    "confidence": "High",
    "flagged_features": [
      "Suspicious keyword 'paypal' in non-official domain",
      "High entropy domain name",
      "Contains 'login' parameter in insecure HTTP connection"
    ],
    "execution_time_ms": 14.2
  }
  ```

#### Endpoint 2: Batch Analysis (CSV Upload)
* **Route:** `POST /api/v1/analyze-batch`
* **Request:** `multipart/form-data` with CSV file containing a list of URLs.
* **Response:** JSON array or downloadable CSV with risk scores and classifications for all submitted items.

---

## 7. User Interface (UI) Requirements

### 7.1 Key Pages & Components
1. **Single URL Scanner (Main View):**
   * Prominent search input bar with an "Analyze URL" button.
   * Real-time validation indicator.
2. **Analysis Result Card:**
   * **Gauge / Radial Progress:** Visual risk score (0% - 100%).
   * **Status Badge:** Green (`SAFE`), Yellow (`SUSPICIOUS`), Red (`MALICIOUS / PHISHING`).
   * **Feature Breakdown List:** Explanation of why the URL was flagged.
3. **Batch URL Analyzer:**
   * Drag-and-drop CSV upload area.
   * Paginated results table with export options (Download CSV/JSON).
4. **Model Performance & Info Section:**
   * Displays model accuracy, precision, recall, and training dataset metrics.

---

## 8. Development Roadmap & Milestones

| Phase | Duration | Deliverables |
| :--- | :--- | :--- |
| **Phase 1: ML Model Development** | Days 1–3 | Data collection, preprocessing, feature extraction module, model training (`scikit-learn`/`xgboost`), export model as `phishing_model.pkl`. |
| **Phase 2: Backend API** | Days 4–5 | Set up FastAPI server, implement feature extraction logic on incoming payload, model loading, and endpoint testing. |
| **Phase 3: Web UI Development** | Days 6–8 | Build frontend dashboard, connect to FastAPI API via fetch/axios, implement gauge charts and CSV upload handler. |
| **Phase 4: Testing & Deployment** | Days 9–10 | Containerize with Docker (or deploy directly to Render/Vercel), conduct live URL tests, document API endpoints. |

---

## 9. Next Steps for Implementation
1. **Prepare Python Environment:** Install `pandas`, `scikit-learn`, `xgboost`, `fastapi`, `uvicorn`, `tldextract`.
2. **Download Baseline Data:** Grab the Kaggle Malicious URLs dataset or query PhishTank API.
3. **Write Feature Extractor Script:** Create a modular Python file `features.py` to parse URLs into structured numerical features.