#!/usr/bin/env python3
# monitoring_service.py

import time
import yaml
import json
from pathlib import Path
import logging
from utils.performance import PerformanceMonitor
import threading
from datetime import datetime

class MonitoringService:
    def __init__(self, config_path='/workspace/configs/monitoring_config.yaml'):
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger('YOLOv8-Monitoring')
        
        # Load configuration
        self.config = self.load_config(config_path)
        
        # Initialize monitoring
        self.performance_monitor = PerformanceMonitor(
            buffer_size=self.config.get('buffer_size', 30)
        )
        
        # Setup results directory
        self.results_dir = Path(self.config.get('results_path', '/workspace/results'))
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize monitoring state
        self.is_monitoring = False
        self.monitoring_interval = self.config.get('monitoring_interval', 1.0)

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/workspace/logs/monitoring.log'),
                logging.StreamHandler()
            ]
        )

    def load_config(self, config_path):
        """Load monitoring configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}

    def start_monitoring(self):
        """Start the monitoring service"""
        self.logger.info("Starting monitoring service...")
        self.is_monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop the monitoring service"""
        self.logger.info("Stopping monitoring service...")
        self.is_monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect performance metrics
                stats = self.performance_monitor.get_stats()
                
                # Log metrics
                self.performance_monitor.log_performance()
                
                # Save metrics to file
                self._save_metrics(stats)
                
                # Wait for next monitoring interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                continue

    def _save_metrics(self, stats):
        """Save metrics to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            metrics_file = self.results_dir / f'metrics_{timestamp}.json'
            
            metrics = {
                'timestamp': timestamp,
                'metrics': stats
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=4)
                
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")

def main():
    # Initialize and start monitoring service
    monitoring_service = MonitoringService()
    
    try:
        monitoring_service.start_monitoring()
        
        # Keep service running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        monitoring_service.stop_monitoring()
        logging.info("Monitoring service stopped by user")

if __name__ == '__main__':
    main()