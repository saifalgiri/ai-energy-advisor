# thermondo
🏠 Home Energy Advisor
An AI-powered web application that provides personalized energy efficiency recommendations for homes using FastAPI, Vue 3 (TypeScript), and local Ollama LLM with live events (SSE) streaming.

📋 Table of Contents

AI Tools

Features

Architecture

Project Structure

Prerequisites

Installation

Configuration

Running the Application

API Documentation

Testing

 # AI Tools 
 
I used mostly Claude for SSE integration and test, and some quick typing tools, however the rest is done by me 


# Architecture 

System design 
Solid principles 
Design patterns 
Interface, Service, Database
Configurations 
Routes 
Components 
Etc



# ✨ Features
Backend

✅ RESTful API with FastAPI

✅ Clean Architecture - Interface-based design with dependency injection, SOILD principles

✅ SQLAlchemy ORM with async support

✅ Database Migrations with Alembic

✅ Pydantic Validation for request/response

✅ Server-Sent Events (SSE) for real-time streaming

✅ Local Ollama Integration for AI recommendations 

✅ Real-time SSE Streaming - recommendations send one-by-one

✅ Logging with Python logging

✅ Unit Tests with pytest and async support

✅ Type Safety throughout the codebase

Frontend

✅ Vue 3 Composition API with TypeScript

✅ Real-time SSE Streaming - recommendations appear one-by-one

✅ Type-safe API Client with full TypeScript interfaces

✅ Vue Componentst with for reuseability and maintainability 

✅ Vue Composables for reusable api logic

✅ Error Handling with user-friendly messages

AI Features

LLM-Powered Analysis using Ollama (llama2:7b or any model)

 Prioritized Recommendations (High/Medium/Low)
 
Cost & Savings Estimates for each recommendation

Auto-Categorization (Heating, Insulation, Windows, etc.)

# 🏗️ Architecture
SOLID principle
Dependency Injection 
Api layer, service layer, database layer and some other custom layers
Fluent validation 
Naming conventions 
Custom exception handling 
Logging

# Assumption
House owners need to provide some details that mostly easy to know
Instruct the AI with clear and structured prompt therefor we can get a better result 
Enable direct interaction from AI to house owner directly

# Tradeoff
1- Currently, every request for energy advice triggers a new analysis call to Ollama. This approach does not scale well and can significantly increase response times when the system is under heavy load (e.g., thousands of concurrent requests). Over time, this can also lead to higher operational complexity and increased costs.
A more efficient solution is to recognize that many house profiles may be identical or highly similar. Instead of calling Ollama for every request, we should persist the AI-generated recommendations in a dedicated database table.
When a new request is received, the system should first check whether an identical (or 100% matching) house profile has already been processed. If a match exists, the stored recommendations can be returned immediately without invoking Ollama. This reduces latency, lowers operational costs, and improves overall system scalability.

2-When navigating back from the recommendations page to the house details page, the frontend should reuse the existing house_id to fetch and prefill the previously created house profile. Any changes should update the existing record rather than creating a new house profile.


# 📦 Prerequisites
Before you begin, ensure you have the following installed:

Required

```
Python: 3.13.1 
Node.js: v22.12.0
Ollama - Download
```
Recommended
Git - For version control
VS Code - With Python and Vue extensions
PostgreSQL 

# 🚀 Installation

```1. Clone Repository
git clone https://github.com/saifalgiri/ai-energy-advisor.git
cd ai-energy-advisor

2. Backend Setup
cd backend
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install test dependencies (optional)
cd  tests
pip install -r requirements-test.txt

3. Frontend Setup

cd frontend
-> pnpm for package management
npm install -g pnpm     
pnpm install

4. Ollama Setup
Local ollama serve
1️⃣ Install Ollama
👉 https://ollama.com
2️⃣ Run LLaMA 2
ollama run llama2:7b

The url for Ollama is:
http://localhost:11434
```


# ⚙️ Configuration
```Backend Configuration

Edit backend/.env:
# Application
APP_NAME=Home Energy Advisor
API_V1_STR=/api/v1

# Database
Create database with name home_energy_db
Change DATABASE_URL `user` and `password` that works for your PC

# `DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/home_energy_db `
Go to file alembic.ini and ensure the database connection is same as .env 
`sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5433/home_energy_db`

# Apply migration
alembic upgrade head

# Ollama

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b
OLLAMA_TIMEOUT=120

# CORS (add backend and  frontend URLs)
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]


Frontend Configuration
Edit frontend/src/config/homeApi.ts:
const API_BASE = 'http://localhost:8000/api/v1';
```

# 🏃 Running the Application

Terminal 1: Start Ollama 

2️⃣ Run LLaMA 2

`ollama run llama2:7b`

The url for Ollama is:

`http://localhost:11434`

Everything already configured in `.env`  file 

Terminal 2: Start Backend

backend 

 `uvicorn app.main:app --reload ` 
 
Backend will be available at:

API: http://localhost:8000
Docs: http://localhost:8000/docs

Terminal 3: Start Frontend

`pnpm dev`


Frontend will be available at:
App: http://localhost:5173
Fill up home details and it will navigate to the recommendation page automatically, wait for Ollama and you will see the results in presentable cards. Sometimes the local Ollama might be timeout so either retry or extend OLLAMA_TIMEOUT=120 in backend .env

# 📖 API Documentation
Interactive Documentation
Once the backend is running, visit:
Swagger UI: http://localhost:8000/docs
Example Requests
Create Home
```curl -X 'POST' \
  'http://localhost:8000/api/v1/homes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "size_sqft": 1500,
  "year_built": 2000,
  "heating_type": "gas",
  "insulation_level": "moderate",
  "windows_type": "double",
  "roof_type": "pitched",
  "monthly_energy_bill": 150,
  "num_occupants": 3,
  "location": ""
}'
```


Get Recommendations (SSE)
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/homes/658304ad-b0d6-4429-95c7-ed1f1646afcc/advice' \
  -H 'accept: application/json' \
  -d ''

SSE Message Format
// Connected
{
  "type": "connected",
  "home_id": "abc123"
}

// Recommendation (streamed one-by-one)
{
  "type": "recommendation",
  "recommendation": {
    "id": "R1",
    "title": "Upgrade Insulation",
    "description": "Add blown-in insulation...",
    "estimated_cost": "2000€",
    "estimated_savings": "320€/year",
    "priority": "high",
    "category": "insulation"
  }
}

// Complete
{
  "type": "complete"
}

// Error
{
  "type": "error",
  "error": "Error message"
}

```

 # Testing
Backend Tests
```cd backend/tests
 venv/bin/activate
pip install -r requirements-test.txt

# Run all tests
pytest
```

# Prompt Engineering 

You are a senior residential energy retrofit consultant.

Your task is to recommend HIGH-IMPACT energy efficiency upgrades that deliver the
LARGEST POSSIBLE annual cost savings within the given constraints.

You are explicitly allowed to recommend:
- Insulation upgrades (roof, walls, floors)
- Heating system replacement or optimization
- Window replacement if justified
- Structural or technical interventions with medium renovation effort

DO NOT recommend:
- Behavioral tips
- Low-impact tweaks (LEDs, reminders, habits)
- Measures saving less than 300 €/year

Energy prices:
- Gas: 0.12 €/kWh
- Electricity: 0.35 €/kWh

Constraints:
- Budget: up to 15,000 €
- Ownership: Owned
- Renovation tolerance: Medium
- Primary goal: Reduce heating costs and improve winter comfort

Home details:
- Size: {home.size_sqft} sq ft
- Age: {home_age} years (built {home.year_built})
- Location: {home.location}
- Heating: {home.heating_type.value}
- Insulation: {home.insulation_level.value}
- Windows: {home.windows_type.value}-pane
- Occupants: {home.num_occupants}
- Monthly_Bill: {home.monthly_energy_bill} Euro

Return ONLY valid JSON in the following structure:
```
{{
  "recommendations": [
    {{
      "id": "R1",
      "priority": "High",
      "details": "Technically specific retrofit action with clear scope",
      "estimate_cost": "Upfront cost range in €",
      "saving_cost": "Estimated annual savings in €/year (must be ≥ 300 €/year)"
    }}
  ]
}}
```
Rules:
- JSON only, no extra text
- 1-4 recommendations
- Prioritize MAXIMUM annual savings, not lowest cost
- All recommendations must meaningfully reduce heating demand
- Be realistic but bold in savings estimates
"""




