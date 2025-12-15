"""
Data processing: CSV loading, analysis, visualization.
All operations use in-memory processing (Phase 3.3).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64
from typing import Optional, Dict, Any
from config import settings

# Global DataFrame storage (session-based in production)
dataframes: Dict[str, pd.DataFrame] = {}


def load_csv(file_content: bytes, filename: str, session_id: str) -> Dict[str, Any]:
    """
    Load CSV from bytes (in-memory, Phase 3.3).
    """
    try:
        # Validate file size
        if len(file_content) > settings.max_file_size_mb * 1024 * 1024:
            raise ValueError(f"File size exceeds maximum of {settings.max_file_size_mb}MB")
        
        # Read CSV from bytes
        df = pd.read_csv(BytesIO(file_content))
        
        # Validate DataFrame size
        if len(df) > settings.max_dataframe_rows:
            raise ValueError(f"DataFrame exceeds maximum of {settings.max_dataframe_rows} rows")
        
        # Store in memory
        dataframes[session_id] = df
        
        return {
            "success": True,
            "rows": len(df),
            "columns": list(df.columns),
            "shape": df.shape,
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_dataframe(session_id: str) -> Optional[pd.DataFrame]:
    """Get DataFrame for session."""
    return dataframes.get(session_id)


def describe_data(session_id: str) -> Dict[str, Any]:
    """Get statistical summary of data."""
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    return {
        "success": True,
        "describe": df.describe().to_dict(),
        "info": {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
    }


def correlation_matrix(session_id: str) -> Dict[str, Any]:
    """Get correlation matrix."""
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) == 0:
        return {"error": "No numeric columns found"}
    
    corr = numeric_df.corr()
    return {
        "success": True,
        "correlation": corr.to_dict(),
        "columns": list(corr.columns)
    }


def head_data(session_id: str, n: int = 5) -> Dict[str, Any]:
    """Get first N rows."""
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    return {
        "success": True,
        "data": df.head(n).to_dict(orient="records"),
        "columns": list(df.columns)
    }


def tail_data(session_id: str, n: int = 5) -> Dict[str, Any]:
    """Get last N rows."""
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    return {
        "success": True,
        "data": df.tail(n).to_dict(orient="records"),
        "columns": list(df.columns)
    }


def info_data(session_id: str) -> Dict[str, Any]:
    """Get DataFrame info."""
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    buffer = BytesIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue().decode('utf-8')
    
    return {
        "success": True,
        "info": info_str,
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "null_counts": df.isnull().sum().to_dict()
    }


def generate_plot(
    session_id: str,
    plot_type: str,
    x: Optional[str] = None,
    y: Optional[str] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    format_type: str = "plotly"  # "plotly" or "image"
) -> Dict[str, Any]:
    """
    Generate plot (in-memory, Phase 3.3).
    Returns Plotly JSON spec or base64-encoded PNG.
    """
    df = get_dataframe(session_id)
    if df is None:
        return {"error": "No dataset loaded"}
    
    try:
        # Clear previous plot
        plt.clf()
        
        # Generate plot based on type
        if plot_type == "bar":
            if x and y:
                # For bar charts, group by X and aggregate Y for better visualization
                # This shows average/mean Y value for each X category
                if df[x].nunique() < df.shape[0]:
                    # Group by x and aggregate y (mean) - better for categorical or repeated x values
                    grouped = df.groupby(x)[y].agg(['mean', 'count']).reset_index()
                    grouped.columns = [x, y, '_count']
                    fig = px.bar(
                        grouped, 
                        x=x, 
                        y=y, 
                        title=title or f"Average {y} by {x}",
                        labels={x: xlabel or x, y: ylabel or f"Average {y}"},
                        text=y,  # Show values on bars
                        text_auto='.2s'  # Format numbers
                    )
                else:
                    # If every x value is unique, use data directly
                    fig = px.bar(
                        df, 
                        x=x, 
                        y=y, 
                        title=title or f"{y} by {x}",
                        labels={x: xlabel or x, y: ylabel or y}
                    )
                # Improve bar chart appearance
                fig.update_traces(
                    marker_color='steelblue',
                    marker_line_color='darkblue',
                    marker_line_width=1.5,
                    opacity=0.85,
                    textposition='outside'
                )
                fig.update_layout(
                    bargap=0.3,
                    xaxis_tickangle=-45 if df[x].dtype == 'object' else 0,
                    height=500,
                    showlegend=False,
                    hovermode='x unified'
                )
            else:
                return {"error": "Bar plot requires x and y parameters"}
        
        elif plot_type == "line":
            if x and y:
                fig = px.line(
                    df, 
                    x=x, 
                    y=y, 
                    title=title or f"{y} over {x}",
                    labels={x: xlabel or x, y: ylabel or y}
                )
                fig.update_traces(line_width=2, marker_size=4)
                fig.update_layout(height=500)
            else:
                return {"error": "Line plot requires x and y parameters"}
        
        elif plot_type == "scatter":
            if x and y:
                fig = px.scatter(
                    df, 
                    x=x, 
                    y=y, 
                    title=title or f"{y} vs {x}",
                    labels={x: xlabel or x, y: ylabel or y}
                )
                fig.update_traces(marker_size=8, opacity=0.6)
                fig.update_layout(height=500)
            else:
                return {"error": "Scatter plot requires x and y parameters"}
        
        elif plot_type == "histogram":
            if x:
                fig = px.histogram(
                    df, 
                    x=x, 
                    title=title or f"Distribution of {x}",
                    labels={x: xlabel or x}
                )
                fig.update_traces(marker_color='steelblue', opacity=0.7)
                fig.update_layout(height=500, showlegend=False)
            else:
                return {"error": "Histogram requires x parameter"}
        
        elif plot_type == "pie":
            if x:
                value_counts = df[x].value_counts()
                fig = px.pie(
                    values=value_counts.values, 
                    names=value_counts.index, 
                    title=title or f"Distribution of {x}"
                )
                fig.update_layout(height=500)
            else:
                return {"error": "Pie chart requires x parameter"}
        
        elif plot_type == "heatmap":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) == 0:
                return {"error": "No numeric columns for heatmap"}
            corr = numeric_df.corr()
            fig = px.imshow(
                corr, 
                title=title or "Correlation Heatmap", 
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu"
            )
            fig.update_layout(height=500)
        
        elif plot_type == "box":
            if x and y:
                fig = px.box(
                    df, 
                    x=x, 
                    y=y, 
                    title=title or f"{y} by {x}",
                    labels={x: xlabel or x, y: ylabel or y}
                )
                fig.update_traces(marker_color='steelblue')
                fig.update_layout(height=500)
            else:
                return {"error": "Box plot requires x and y parameters"}
        
        else:
            return {"error": f"Unknown plot type: {plot_type}"}
        
        # Update labels (if not already set in plot creation)
        if xlabel and not hasattr(fig, '_xlabel_set'):
            fig.update_xaxes(title=xlabel)
        if ylabel and not hasattr(fig, '_ylabel_set'):
            fig.update_yaxes(title=ylabel)
        
        # Apply consistent styling to all plots
        fig.update_layout(
            template='plotly_white',
            font=dict(size=12),
            title_font_size=16,
            margin=dict(l=60, r=20, t=60, b=60)
        )
        
        # Return based on format
        if format_type == "plotly":
            # Return Plotly JSON spec (Phase 5.2)
            return {
                "success": True,
                "format": "plotly",
                "spec": fig.to_dict(),
                "data": df.to_dict(orient="records")  # Include data for client-side filtering
            }
        else:
            # Return base64-encoded PNG (fallback)
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            return {
                "success": True,
                "format": "image",
                "mime": "image/png",
                "base64": img_base64
            }
    
    except Exception as e:
        return {"error": str(e)}


def clear_session(session_id: str):
    """Clear session data."""
    if session_id in dataframes:
        del dataframes[session_id]

