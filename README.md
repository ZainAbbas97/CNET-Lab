# Python Data Analysis and Visualization System

This project implements and improves upon the research paper "Python Data Analysis and Visualization in Java GUI Applications Through TCP Socket Programming" by Bala Dhandayuthapani V.

## Project Structure

```
.
├── baseline/              # Original TCP socket implementation
│   ├── python_server.py  # Python TCP server
│   ├── java_client/      # Java GUI clients (Swing)
│   └── data/             # Sample datasets
├── improved/             # Modern web-based implementation
│   ├── backend/          # FastAPI Python backend
│   ├── frontend/         # React TypeScript frontend
│   └── docker/           # Docker configuration
├── docs/                 # Documentation
│   ├── BASELINE_REPRODUCTION.md
│   ├── SYSTEM_ANALYSIS.md
│   ├── IMPROVEMENT_ROADMAP.md
│   └── IMPLEMENTATION_CHECKLIST.md
└── research_paper.pdf    # Original research paper
```

## Quick Start

### Baseline System (Original TCP Socket)

See `baseline/README.md` for detailed instructions.

```bash
# Python server
cd baseline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate_data.py  # Generate sample data
python python_server.py

# Java client (in separate terminal)
cd baseline/java_client
javac JavaClientSwing.java
java JavaClientSwing
```

### Improved System (Web-based) - **RECOMMENDED**

See `improved/GETTING_STARTED.md` for detailed instructions.

**Option 1: Docker Compose (Easiest)**

```bash
cd improved
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Option 2: Manual Setup**

```bash
# Backend
cd improved/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# Frontend (new terminal)
cd improved/frontend
npm install
cp .env.example .env
npm run dev
```

## Features

### Baseline System
- TCP socket communication
- Python server with Matplotlib/Seaborn
- Java Swing GUI client
- Static image visualizations

### Improved System
- ✅ **Zero-install**: Browser-based, no Java/Python installation needed
- ✅ **Security**: Command whitelisting, input validation, rate limiting
- ✅ **Interactive**: Plotly.js visualizations with zoom, pan, hover
- ✅ **Modern API**: RESTful HTTP/JSON + WebSocket support
- ✅ **In-memory**: No disk I/O, faster performance
- ✅ **Concurrent**: Supports multiple users
- ✅ **Type-safe**: TypeScript frontend, type hints in backend

## Documentation

### Comparison Documents (NEW!)
- **Executive Summary**: `EXECUTIVE_SUMMARY.md` - High-level comparison overview
- **Comparison Report**: `docs/COMPARISON_REPORT.md` - Comprehensive comparison with graphs
- **Visual Comparison**: `docs/VISUAL_COMPARISON.md` - Visual charts and explanations
- **Generated Charts**: `docs/comparison_charts.png` and `docs/improvement_percentages.png`

### Technical Documentation
- **Baseline Reproduction**: `docs/BASELINE_REPRODUCTION.md` - How to reproduce the paper's results
- **System Analysis**: `docs/SYSTEM_ANALYSIS.md` - Weakness diagnosis and data flow
- **Improvement Roadmap**: `docs/IMPROVEMENT_ROADMAP.md` - Phased improvement plan
- **Implementation Checklist**: `docs/IMPLEMENTATION_CHECKLIST.md` - Detailed checklist
- **Getting Started**: `improved/GETTING_STARTED.md` - Quick start guide

## Comparison

| Feature | Baseline | Improved |
|---------|----------|----------|
| Installation | Java + Python required | Browser only |
| Security | None (arbitrary code execution) | Whitelisted commands, validation |
| Visualizations | Static images | Interactive (Plotly) |
| Protocol | TCP socket | HTTP/JSON + WebSocket |
| Concurrency | Single client | Multiple clients |
| Performance | File I/O overhead | In-memory processing |
| Error Handling | Basic | Comprehensive |
| API Documentation | None | Auto-generated (OpenAPI) |

## Implementation Status

### ✅ Completed (Phases 1-3)
- Phase 1: Security fixes (whitelisting, validation, limits)
- Phase 2: Protocol modernization (HTTP/JSON, WebSocket)
- Phase 3: Architecture redesign (FastAPI, React, in-memory)

### 🔄 Future Phases
- Phase 4: Security hardening (TLS, JWT, sandboxing)
- Phase 5: Enhanced visualizations (data + spec approach)
- Phase 6: Performance optimization (compression, caching)
- Phase 7: Developer experience (SDK, testing, docs)

## Requirements

### Baseline
- Python 3.9+
- Java 11+
- pandas, matplotlib, seaborn, numpy

### Improved
- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- Docker & Docker Compose (optional, recommended)

## License

This project is for educational purposes, implementing and improving upon the research paper.

## References

- Research Paper: "Python Data Analysis and Visualization in Java GUI Applications Through TCP Socket Programming" by Bala Dhandayuthapani V.
- Published in: International Journal of Information Technology and Computer Science, Volume 16, Issue 3, June 2024
- DOI: 10.5815/ijitcs.2024.03.07
