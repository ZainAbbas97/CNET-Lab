# Baseline Implementation - TCP Socket System

This directory contains the baseline reproduction of the research paper's system using TCP socket programming.

## Files

- `python_server.py` - Python TCP server that processes commands
- `java_client/JavaClientSwing.java` - Java Swing GUI client
- `generate_data.py` - Script to generate sample dataset
- `data/data.csv` - Sample dataset (generated)

## Setup

### Python Server

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_data.py

# Start server
python python_server.py
```

### Java Client

```bash
cd java_client
javac JavaClientSwing.java
java JavaClientSwing
```

## Usage

1. Start the Python server first
2. Run the Java client
3. In the Java GUI:
   - Enter `data.csv` and click Send (to load dataset)
   - Enter matplotlib/seaborn plotting commands, e.g.:
     ```
     plt.bar(df['rooms'], df['price'])
     plt.title("House Price")
     plt.xlabel('Rooms')
     plt.ylabel('Prices')
     ```
   - Enter `chart` and click Send (to generate and display plot)

## Protocol

- **CSV Loading**: Send filename ending with `.csv`
- **Chart Generation**: Send `chart` command
- **Python Execution**: Send any Python code (executed via exec())
- **Exit**: Send `exit` or `quit`

## Limitations (As Per Paper)

- Static visualizations only
- No security (arbitrary code execution)
- Single client connection
- File I/O required for image transfer
- No error recovery





