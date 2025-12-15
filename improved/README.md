# Improved System - Web-Based Data Visualization

This is the improved implementation with FastAPI backend and React frontend, implementing Phases 1-3 of the improvement roadmap.

## Features Implemented

### Phase 1: Security Fixes
- ✅ Command whitelisting (no arbitrary code execution)
- ✅ Input validation and sanitization
- ✅ File size and command length limits

### Phase 2: Protocol Modernization
- ✅ HTTP/JSON REST API
- ✅ WebSocket support for real-time updates
- ✅ Structured request/response format

### Phase 3: Architecture Redesign
- ✅ FastAPI backend with async support
- ✅ React + TypeScript frontend (zero-install)
- ✅ In-memory processing (no disk I/O)
- ✅ Interactive Plotly visualizations

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd improved
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend

```bash
cd improved/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy .env.example to .env and configure
cp .env.example .env

# Run server
uvicorn main:app --reload
```

#### Frontend

```bash
cd improved/frontend
npm install

# Copy .env.example to .env
cp .env.example .env

# Run development server
npm run dev
```

## Usage

1. **Upload Dataset**: Drag and drop a CSV file or click to select
2. **Execute Commands**: Use the command panel to:
   - `plot` - Generate visualizations (bar, line, scatter, histogram, pie, heatmap, box)
   - `describe` - Get statistical summary
   - `corr` - Get correlation matrix
   - `head` / `tail` - View first/last N rows
   - `info` - Get DataFrame information
3. **View Results**: 
   - Text output appears in the output panel
   - Interactive plots appear in the visualization panel

## API Endpoints

- `POST /api/v1/upload` - Upload CSV dataset
- `POST /api/v1/execute` - Execute whitelisted command
- `GET /api/v1/data/describe` - Statistical summary
- `GET /api/v1/data/corr` - Correlation matrix
- `GET /api/v1/health` - Health check
- `WS /api/v1/ws` - WebSocket for real-time updates

See `/docs` for interactive API documentation.

## Security Features

- Command whitelisting (no arbitrary code execution)
- Input validation and sanitization
- File size limits (100MB max)
- Rate limiting (100 req/min per IP)
- CORS protection
- Filename sanitization (no path traversal)

## Configuration

See `backend/.env.example` for all configuration options.

## Development

### Backend
- FastAPI with automatic OpenAPI docs
- Type hints throughout
- Async/await support
- In-memory data processing

### Frontend
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- React Query for data fetching
- Plotly.js for interactive visualizations

## Next Steps (Future Phases)

- Phase 4: TLS encryption, JWT authentication, sandboxed execution
- Phase 5: Enhanced visualizations, data + spec approach
- Phase 6: Compression, caching, benchmarking
- Phase 7: TypeScript SDK, comprehensive testing, documentation





