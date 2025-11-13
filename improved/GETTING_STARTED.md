# Getting Started Guide

This guide will help you get the improved data visualization system up and running in under 5 minutes.

## Prerequisites

- **Docker & Docker Compose** (recommended), OR
- **Python 3.11+** and **Node.js 18+** (for manual setup)

## Quick Start with Docker (Recommended)

### Step 1: Navigate to the improved directory

```bash
cd improved
```

### Step 2: Start all services

```bash
docker-compose up
```

This will start:
- Backend API server (http://localhost:8000)
- Frontend web app (http://localhost:3000)
- Redis cache (optional, for future use)

### Step 3: Open the application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

### Step 4: Upload a dataset

1. Click or drag & drop a CSV file in the "Upload Dataset" area
2. Wait for the upload to complete
3. You'll see the dataset info (rows, columns) in the header

### Step 5: Generate a visualization

1. In the Command Panel, select "plot" command
2. Choose a plot type (bar, line, scatter, etc.)
3. Enter column names for X and Y axes
4. Click "Execute Command"
5. View the interactive plot in the Visualization panel

## Manual Setup (Without Docker)

### Backend Setup

```bash
# Navigate to backend directory
cd improved/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env

# Start server
uvicorn main:app --reload
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd improved/frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Example Usage

### 1. Upload Dataset

Use the sample dataset from the baseline system:
```bash
# Generate sample data
cd ../../baseline
python generate_data.py

# Upload data.csv through the web interface
```

### 2. Execute Commands

**Describe data:**
- Command: `describe`
- No parameters needed
- Shows statistical summary

**Correlation matrix:**
- Command: `corr`
- No parameters needed
- Shows correlation between numeric columns

**Generate plot:**
- Command: `plot`
- Parameters:
  - `type`: "bar", "line", "scatter", "histogram", "pie", "heatmap", "box"
  - `x`: Column name for X axis
  - `y`: Column name for Y axis (optional for some plot types)
  - `title`: Plot title (optional)

**View data:**
- Command: `head` or `tail`
- Parameters: `n` (number of rows, default: 5)

**DataFrame info:**
- Command: `info`
- No parameters needed
- Shows data types, null counts, memory usage

## Troubleshooting

### Port already in use

If port 8000 or 3000 is already in use:

**Backend:**
```bash
# Change port in .env file
PORT=8001
```

**Frontend:**
```bash
# Change port in vite.config.ts
server: {
  port: 3001,
}
```

### CORS errors

Make sure the frontend URL is in the backend's `CORS_ORIGINS` setting:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Dataset not loading

- Check file size (max 100MB)
- Ensure file is valid CSV
- Check browser console for errors
- Verify backend is running

### Plot not displaying

- Check that columns exist in dataset
- Verify column names match exactly (case-sensitive)
- Check browser console for errors
- Try a different plot type

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Try different plot types and commands
- Upload your own datasets
- Check out the improvement roadmap in `docs/IMPROVEMENT_ROADMAP.md`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API documentation
3. Check the system analysis in `docs/SYSTEM_ANALYSIS.md`

