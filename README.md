# Project Context: Phishing URL Detector

## Quick Overview

* **Project Goal:** Full-stack cybersecurity web application to detect phishing and malicious URLs in real-time using Machine Learning.

* **Key Features:**

  1. Single URL Analysis with real-time risk score gauge and flagged indicators.

  2. Batch processing via CSV file upload.

  3. Model performance overview dashboard.

* **Core Workflow:**
  `User URL Input` -> `FastAPI Backend` -> `Lexical Feature Extractor` -> `ML Model Inference (.pkl)` -> `JSON Response` -> `Frontend Dashboard`

## Tech Stack Summary

* **ML / Data:** Python, `scikit-learn`, `XGBoost`, `pandas`, `joblib`

* **Backend:** `FastAPI`, `pydantic`, `uvicorn`

* **Frontend:** Modern Web UI (React/Next.js or HTML5 + Tailwind CSS + Vanilla JS)

* **Deployment:** Render / Railway / Hugging Face Spaces

## Key Targets & Constraints

* **Inference Speed:** < 100ms per URL.

* **Target Accuracy:** F1-Score >= 95%.

* **Output Standard:** Predicts label (`Legitimate` vs `Phishing`), confidence score (0.0 - 1.0), and a list of specific suspicious features detected.