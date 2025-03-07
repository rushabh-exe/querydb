# querydb - Natural Language Database Interface

querydb is a full-stack application that enables natural language interactions with databases, combining AI-powered query generation with dynamic data visualization. It bridges the gap between human language and SQL queries, making database interactions accessible to non-technical users.

## Architecture

### Backend (Python/Flask)
- **Core Components:**
  - Query Processing API (`/api/v1/query`)
  - LLM Integration (supports both local Ollama and Groq)
  - PostgreSQL Database Connection
  - Dynamic Visualization Processing

### Frontend (React/Vite)
- **Features:**
  - Interactive Query Interface
  - Real-time Data Visualization
  - Support for Tables, Graphs, and Pie Charts
  - Human-Readable Response Generation

## Key Features

### 1. Natural Language Query Processing
- Converts natural language questions into SQL queries
- Handles complex database schema understanding
- Provides context-aware query generation

### 2. Dynamic Visualization
Automatically selects and renders the most appropriate visualization type:
- **Tables:** For structured data display
- **Graphs:** For trend analysis and time-series data
- **Pie Charts:** For distribution and proportion analysis

### 3. AI Integration
- Dual LLM support:
  - Local deployment via Ollama
  - Cloud-based using Groq
- Intelligent visualization selection
- Natural language result summarization

### 4. Database Integration
- PostgreSQL support with automatic schema analysis
- Real-time query execution
- Secure connection handling
- Type conversion and data formatting

## Technical Setup

### Backend Requirements
```txt
flask
python-dotenv
psycopg2-binary
ollama
flask_cors
groq
```

### Frontend Dependencies
- React 18.3
- Recharts for visualization
- TailwindCSS for styling
- Vite for build tooling

## Environment Configuration
Required environment variables:
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5431
ALLOWED_ORIGINS=http://localhost:5173
LLM_MODEL=model-name
LOG_LEVEL=INFO
GROQ_API_KEY=your_groq_api_key
```

## Docker Support
Both frontend and backend components include Docker configurations for containerized deployment:

### Backend Container
- Python 3.9 slim-based image
- Exposes ports 8000, 5431, 5173, 11434
- Includes PostgreSQL client libraries

### Frontend Container
- Node 20 Alpine-based image
- Exposes port 5173
- Development server with HMR support

## Getting Started

1. Clone the repository
2. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Start the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   python run.py
   ```
4. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Docker Deployment
```bash
# Backend
cd backend
docker build -t query-backend .
docker run -p 8000:8000 query-backend

# Frontend
cd frontend
docker build -t query-frontend .
docker run -p 5173:5173 query-frontend
```

## Project Structure
```
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   └── assets/
    └── package.json
```
