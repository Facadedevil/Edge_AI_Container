# utils/visualization.py

import plotly.graph_objs as go
from dash import html, dcc

def create_plot(data, title, y_axis_title, plot_type='scatter'):
    """Create a plotly figure with common styling"""
    
    if plot_type == 'scatter':
        trace = go.Scatter(
            y=data,
            mode='lines+markers',
            marker=dict(size=6),
            line=dict(width=2)
        )
    elif plot_type == 'bar':
        trace = go.Bar(y=data)
    
    layout = go.Layout(
        title=title,
        yaxis_title=y_axis_title,
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        showlegend=False
    )
    
    return {'data': [trace], 'layout': layout}

def create_dashboard_layout():
    """Create a standard dashboard layout"""
    return html.Div([
        # Header
        html.Div([
            html.H1('YOLOv8 Performance Dashboard',
                   style={'textAlign': 'center', 'color': 'white'})
        ], style={'backgroundColor': '#1e1e1e', 'padding': '20px'}),
        
        # Main content
        html.Div([
            # Performance Section
            html.Div([
                html.H3('Performance Metrics',
                        style={'color': 'white', 'marginBottom': '20px'}),
                html.Div([
                    dcc.Graph(id='fps-graph', className='graph-container'),
                    dcc.Graph(id='latency-graph', className='graph-container')
                ], style={'display': 'flex'})
            ], className='metric-section'),
            
            # Resource Usage Section
            html.Div([
                html.H3('Resource Usage',
                        style={'color': 'white', 'marginBottom': '20px'}),
                html.Div([
                    dcc.Graph(id='gpu-graph', className='graph-container'),
                    dcc.Graph(id='memory-graph', className='graph-container')
                ], style={'display': 'flex'})
            ], className='metric-section'),
            
            # System Health Section
            html.Div([
                html.H3('System Health',
                        style={'color': 'white', 'marginBottom': '20px'}),
                html.Div([
                    dcc.Graph(id='temp-graph', className='graph-container'),
                    dcc.Graph(id='cpu-graph', className='graph-container')
                ], style={'display': 'flex'})
            ], className='metric-section')
        ], style={'padding': '20px'})
    ], style={'backgroundColor': '#2b2b2b', 'minHeight': '100vh'})