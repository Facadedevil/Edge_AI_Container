#!/usr/bin/env python3
# visualization_service.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime, timedelta
import numpy as np

class DashboardService:
    def __init__(self, results_dir='/workspace/results'):
        self.results_dir = Path(results_dir)
        self.setup_logging()
        self.app = self.create_dash_app()

    def setup_logging(self):
        """Setup logging for visualization service"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/workspace/logs/visualization.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('YOLOv8-Visualization')

    def load_metrics(self, time_window=300):  # 5 minutes window
        """Load metrics from files within time window"""
        metrics_data = []
        current_time = datetime.now()
        
        try:
            for metrics_file in self.results_dir.glob('metrics_*.json'):
                # Check if file is within time window
                file_time = datetime.strptime(metrics_file.stem.split('_')[1], '%Y%m%d_%H%M%S')
                if current_time - file_time <= timedelta(seconds=time_window):
                    with open(metrics_file, 'r') as f:
                        data = json.load(f)
                        metrics_data.append(data)
        except Exception as e:
            self.logger.error(f"Error loading metrics: {e}")
            
        return pd.DataFrame(metrics_data)

    def create_dash_app(self):
        """Create and configure Dash application"""
        app = dash.Dash(__name__)
        
        app.layout = html.Div([
            html.H1('YOLOv8 Performance Dashboard',
                   style={'textAlign': 'center', 'margin-bottom': '20px'}),
            
            # Performance Metrics Section
            html.Div([
                html.H3('Real-time Performance Metrics'),
                html.Div([
                    # FPS Graph
                    dcc.Graph(id='fps-graph', style={'width': '50%', 'display': 'inline-block'}),
                    # Processing Time Graph
                    dcc.Graph(id='processing-time-graph', style={'width': '50%', 'display': 'inline-block'})
                ]),
                
                # GPU Metrics Section
                html.Div([
                    # GPU Usage Graph
                    dcc.Graph(id='gpu-usage-graph', style={'width': '50%', 'display': 'inline-block'}),
                    # Memory Usage Graph
                    dcc.Graph(id='memory-usage-graph', style={'width': '50%', 'display': 'inline-block'})
                ]),
                
                # System Metrics
                html.Div([
                    # CPU Usage
                    dcc.Graph(id='cpu-usage-graph', style={'width': '50%', 'display': 'inline-block'}),
                    # Temperature
                    dcc.Graph(id='temperature-graph', style={'width': '50%', 'display': 'inline-block'})
                ])
            ]),
            
            # Update interval
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # in milliseconds
                n_intervals=0
            )
        ])
        
        self.setup_callbacks(app)
        return app

    def setup_callbacks(self, app):
        """Setup Dash callbacks for real-time updates"""
        
        @app.callback(
            [Output('fps-graph', 'figure'),
             Output('processing-time-graph', 'figure'),
             Output('gpu-usage-graph', 'figure'),
             Output('memory-usage-graph', 'figure'),
             Output('cpu-usage-graph', 'figure'),
             Output('temperature-graph', 'figure')],
            Input('interval-component', 'n_intervals')
        )
        def update_graphs(n):
            df = self.load_metrics()
            
            # FPS Graph
            fps_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.fps'], mode='lines+markers')],
                layout=go.Layout(
                    title='Frames Per Second',
                    yaxis_title='FPS',
                    template='plotly_dark'
                )
            )
            
            # Processing Time Graph
            proc_time_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.processing_time'].apply(lambda x: x*1000),
                               mode='lines+markers')],
                layout=go.Layout(
                    title='Processing Time',
                    yaxis_title='Time (ms)',
                    template='plotly_dark'
                )
            )
            
            # GPU Usage Graph
            gpu_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.gpu_load'], mode='lines+markers')],
                layout=go.Layout(
                    title='GPU Utilization',
                    yaxis_title='Usage (%)',
                    template='plotly_dark'
                )
            )
            
            # Memory Usage Graph
            memory_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.gpu_memory_used'], mode='lines+markers',
                               name='Used Memory'),
                      go.Scatter(y=df['metrics.gpu_memory_total'], mode='lines',
                               name='Total Memory')],
                layout=go.Layout(
                    title='GPU Memory Usage',
                    yaxis_title='Memory (MB)',
                    template='plotly_dark'
                )
            )
            
            # CPU Usage Graph
            cpu_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.cpu_percent'], mode='lines+markers')],
                layout=go.Layout(
                    title='CPU Utilization',
                    yaxis_title='Usage (%)',
                    template='plotly_dark'
                )
            )
            
            # Temperature Graph
            temp_fig = go.Figure(
                data=[go.Scatter(y=df['metrics.gpu_temperature'], mode='lines+markers')],
                layout=go.Layout(
                    title='GPU Temperature',
                    yaxis_title='Temperature (°C)',
                    template='plotly_dark'
                )
            )
            
            return fps_fig, proc_time_fig, gpu_fig, memory_fig, cpu_fig, temp_fig

    def run(self, host='0.0.0.0', port=8050, debug=False):
        """Run the dashboard server"""
        self.logger.info(f"Starting visualization server on {host}:{port}")
        self.app.run_server(host=host, port=port, debug=debug)

def main():
    """Entry point for visualization service"""
    dashboard = DashboardService()
    dashboard.run()

if __name__ == '__main__':
    main()