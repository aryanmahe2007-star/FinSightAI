# FinSightAI – AI-Powered Financial Intelligence Platform

<p align="center">
  <strong>Transforming Financial Data into Intelligent Business Decisions.</strong>
</p>

<p align="center">
  An AI-powered financial intelligence and decision-support platform designed to help businesses understand their financial position, identify unusual patterns, forecast cash flow, and make smarter financial decisions.
</p>

---

## Overview

**FinSightAI** is a financial intelligence platform built using Python, Streamlit, Machine Learning, and Large Language Models.

Traditional financial management often involves manually analyzing transactions, tracking expenses, and estimating future cash positions. FinSightAI simplifies this process by combining financial analytics, predictive modeling, anomaly detection, and AI-powered assistance into one interactive dashboard.

The platform transforms raw financial transaction data into meaningful insights that support better financial planning and decision-making.

## Key Features

### 1. Interactive Financial Dashboard
- Centralized overview of business financial performance.
- Total income, expenses, and estimated balance.
- Interactive financial charts and visualizations.
- Recent transaction activity.
- Clear presentation of important financial indicators.

### 2. Cash Flow Predictor
- Forecasts future cash inflows and outflows.
- Estimates upcoming closing balances.
- Helps businesses understand their expected cash position.
- Supports short-term financial planning.

### 3. AI-Based Anomaly Detection
- Uses the Isolation Forest machine learning algorithm.
- Identifies unusual transaction patterns.
- Highlights potentially unexpected financial activities.
- Provides anomaly-related insights for further investigation.

*Note: Anomaly detection identifies unusual patterns; it does not automatically establish fraudulent activity.*

### 4. Business Health Analysis
- Calculates an overall Business Health Score out of 100.
- Evaluates reserve strength, expense coverage, and cash flow consistency.
- Provides financial runway and coverage indicators.
- Helps assess the financial stability of a business.

### 5. AI Finance Copilot
- Interactive financial assistant powered by a Large Language Model.
- Allows users to ask financial questions in natural language.
- Generates insights using available financial transaction data.
- Uses Ollama with the Qwen 2.5 3B model for local AI inference.

### 6. Smart Purchase Planner
- Evaluates the financial impact of planned purchases.
- Considers projected balance and required financial reserves.
- Provides purchase-risk assessments and recommendations.
- Supports more informed business spending decisions.

### 7. Transaction Management
- Loads financial transaction records from CSV data.
- Provides access to historical transaction information.
- Supports financial analysis across transaction records.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing and analysis |
| Plotly | Interactive charts and visualizations |
| Scikit-learn | Machine learning and anomaly detection |
| Ollama | Local AI model execution |
| Qwen 2.5 3B | AI-powered financial assistance |
| CSV | Transaction data storage |

## Project Architecture

The project follows a modular architecture to separate the user interface, financial data operations, and intelligent analysis.

```text
FinSightAI/
│
├── app.py
│   └── Streamlit frontend and dashboard
│
├── database.py
│   └── Transaction data loading and processing
│
├── ai_engine.py
│   └── Financial intelligence and machine learning
│
├── local_copilot.py
│   └── Local AI finance assistant
│
├── data/
│   └── transactions.csv
│
├── .venv/
│   └── Python virtual environment
│
├── requirements.txt
│
└── README.md
```

## AI and Analytical Components

FinSightAI integrates multiple analytical techniques:

- **Cash Flow Forecasting:** Uses historical transaction information to estimate future financial activity.
- **Isolation Forest:** Detects unusual transaction patterns using unsupervised machine learning.
- **Business Health Scoring:** Combines multiple financial indicators into an overall score.
- **Large Language Model:** Uses Qwen 2.5 3B through Ollama for natural-language financial assistance.
- **Purchase Risk Analysis:** Evaluates planned spending against projected cash availability and reserve requirements.

## Installation and Setup

Follow these steps to run FinSightAI locally.

### Prerequisites

Make sure you have installed:

- Python 3.10 or newer
- Git
- Ollama
- Qwen 2.5 3B model

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/FinSightAI.git
```

Navigate into the project folder:

```bash
cd FinSightAI
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Local AI Model

Install Ollama from:

https://ollama.com/

Download the Qwen 2.5 3B model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before using the AI Finance Copilot.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

The FinSightAI dashboard should now be available in your browser.

---

## Dataset

FinSightAI uses transaction data stored in CSV format.

The dataset contains financial transaction information used for:
- Income and expense analysis.
- Cash flow forecasting.
- Anomaly detection.
- Business health evaluation.
- AI-powered financial insights.

The application expects the transaction dataset at:

```text
data/transactions.csv
```

Use synthetic or anonymized financial data when sharing or deploying the project publicly.

## Future Enhancements

Potential improvements include:

- Cloud deployment with a custom domain.
- Secure user authentication and role-based access.
- Database integration for persistent financial records.
- Real-time financial data synchronization.
- Advanced forecasting models.
- Multi-business financial analytics.
- Exportable financial reports.
- Improved AI-generated business recommendations.

## Project Objective

The primary objective of FinSightAI is to make financial intelligence more accessible by combining traditional financial analytics with modern AI and machine learning techniques.

It aims to move beyond basic transaction tracking and provide a smarter way to understand financial performance, anticipate potential cash flow challenges, and support informed business decisions.

## Disclaimer

FinSightAI is an analytical and decision-support project. Its forecasts and recommendations are estimates based on available transaction data and configured assumptions. They should not be treated as guaranteed financial outcomes or professional financial advice.

## Author

**FinSightAI – AI-Powered Financial Intelligence Platform**

Developed as a project exploring the integration of Python, machine learning, financial analytics, and locally hosted AI models.
