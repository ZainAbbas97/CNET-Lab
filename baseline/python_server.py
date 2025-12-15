"""
Python TCP Server - Baseline Implementation
Reverse-engineered from the research paper's algorithm description.

This server accepts TCP connections and processes commands:
- CSV file loading (filename.csv)
- Chart generation (chart command)
- Python code execution (exec())
- Exit/quit commands
"""
import socket
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os
import sys
import io
import traceback

# Configuration (from paper analysis)
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 24576  # Minimum buffer size mentioned in paper

# Global DataFrame storage (paper uses 'df' as variable name)
df = None

def setup_plot():
    """Initialize matplotlib figure for plotting."""
    plt.figure(figsize=(8, 6), dpi=100)
    plt.clf()  # Clear any existing plots

def process_csv_command(filename):
    """Load CSV file and create DataFrame."""
    global df
    try:
        if not os.path.exists(filename):
            return f"Error: File '{filename}' not found"
        
        df = pd.read_csv(filename)
        return f"CSV loaded successfully. Shape: {df.shape}"
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

def process_chart_command():
    """Generate and save plot as plot.jpg, return image bytes."""
    global df
    
    if df is None:
        return None, "Error: No dataset loaded. Please load a CSV file first."
    
    try:
        # Check if plot.jpg exists and remove it
        plot_file = 'plot.jpg'
        if os.path.exists(plot_file):
            os.remove(plot_file)
        
        # Save current figure
        plt.savefig(plot_file, format='jpg', dpi=100, bbox_inches='tight')
        
        # Read image file and return bytes
        with open(plot_file, 'rb') as f:
            img_data = f.read()
        
        return img_data, None
    except Exception as e:
        return None, f"Error generating chart: {str(e)}"

def capture_exec_output(code):
    """Execute Python code and capture output."""
    global df
    
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    try:
        # Execute code in global namespace with df available
        exec(code, {'df': df, 'pd': pd, 'plt': plt, 'sns': sns, 'np': pd.np if hasattr(pd, 'np') else __import__('numpy'), 'math': math})
        output = buffer.getvalue()
        
        # If no output, try to get return value
        if not output.strip():
            # Try to evaluate as expression
            try:
                result = eval(code, {'df': df, 'pd': pd, 'plt': plt, 'sns': sns, 'np': pd.np if hasattr(pd, 'np') else __import__('numpy'), 'math': math})
                if result is not None:
                    output = str(result)
            except:
                pass
        
        return output if output else "Command executed successfully"
    except Exception as e:
        return f"Error: {str(e)}\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout

def handle_client(conn, addr):
    """Handle a single client connection."""
    global df
    
    print(f"Connection from {addr}")
    
    try:
        # Receive command
        data = conn.recv(BUFFER_SIZE)
        if not data:
            return
        
        code = data.decode('utf-8').strip()
        print(f"Received command: {code[:100]}...")
        
        # Process exit/quit commands
        if code.lower() in ['exit', 'quit']:
            print(f"Client {addr} requested exit")
            conn.send(b"Server shutting down")
            conn.close()
            return False
        
        # Process CSV loading
        if code.endswith('.csv'):
            response = process_csv_command(code)
            conn.send(response.encode('utf-8'))
        
        # Process chart generation
        elif code == 'chart':
            img_data, error = process_chart_command()
            if error:
                conn.send(error.encode('utf-8'))
            else:
                # Send image size first, then image data
                size = len(img_data)
                conn.send(size.to_bytes(4, byteorder='big'))
                conn.send(img_data)
        
        # Process Python code execution
        else:
            output = capture_exec_output(code)
            # Limit output size to prevent buffer overflow
            if len(output) > BUFFER_SIZE:
                output = output[:BUFFER_SIZE] + "\n... (truncated)"
            conn.send(output.encode('utf-8'))
    
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(error_msg)
        try:
            conn.send(error_msg.encode('utf-8'))
        except:
            pass
    
    finally:
        conn.close()
    
    return True

def main():
    """Main server loop."""
    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Python TCP Server listening on {HOST}:{PORT}")
        print("Waiting for connections...")
        print("Commands: 'filename.csv' to load, 'chart' to generate plot, 'exit' to quit")
        
        while True:
            conn, addr = s.accept()
            should_continue = handle_client(conn, addr)
            if not should_continue:
                break
    
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        s.close()
        print("Server closed")

if __name__ == '__main__':
    main()





