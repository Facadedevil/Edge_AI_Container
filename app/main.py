#!/usr/bin/env python3
# main.py

import argparse
import yaml
import logging
import sys
from pathlib import Path
from realtime_detector import RealtimeObjectDetector
from monitoring_service import MonitoringService
import threading

class YOLOApplication:
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger('YOLOv8-Main')
        self.parse_arguments()
        self.load_config()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path('/workspace/logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'yolo_app.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='YOLOv8 Real-time Detection System')
        parser.add_argument(
            '--config',
            type=str,
            default='/workspace/configs/detector_config.yaml',
            help='Path to configuration file'
        )
        parser.add_argument(
            '--source',
            type=int,
            default=0,
            help='Camera source (default: 0)'
        )
        parser.add_argument(
            '--enable-monitoring',
            action='store_true',
            help='Enable performance monitoring'
        )
        self.args = parser.parse_args()

    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.args.config, 'r') as f:
                self.config = yaml.safe_load(f)
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            sys.exit(1)

    def start_monitoring_service(self):
        """Start the monitoring service in a separate thread"""
        if self.args.enable_monitoring:
            self.logger.info("Starting monitoring service...")
            self.monitoring_service = MonitoringService()
            self.monitoring_thread = threading.Thread(
                target=self.monitoring_service.start_monitoring
            )
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()

    def initialize_detector(self):
        """Initialize the YOLOv8 detector"""
        try:
            self.detector = RealtimeObjectDetector(
                model_path=self.config['model_path'],
                conf_threshold=self.config['conf_threshold'],
                buffer_size=self.config['buffer_size']
            )
            self.logger.info("Detector initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing detector: {e}")
            return False

    def run(self):
        """Main application run method"""
        # Start monitoring if enabled
        self.start_monitoring_service()

        # Initialize detector
        if not self.initialize_detector():
            return

        # Start real-time detection
        try:
            self.logger.info("Starting real-time detection...")
            self.detector.process_camera(
                source=self.args.source,
                display_stats=self.config['display_stats']
            )
        except KeyboardInterrupt:
            self.logger.info("Application stopped by user")
        except Exception as e:
            self.logger.error(f"Error during detection: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        # Stop monitoring service if running
        if self.args.enable_monitoring:
            try:
                self.monitoring_service.stop_monitoring()
                self.monitoring_thread.join()
            except Exception as e:
                self.logger.error(f"Error stopping monitoring service: {e}")

        # Get and log final performance stats
        try:
            stats = self.detector.get_performance_stats()
            self.logger.info("Final Performance Statistics:")
            self.logger.info(f"Average FPS: {stats['fps']:.1f}")
            self.logger.info(f"Average Processing Time: {stats['processing_time']*1000:.1f}ms")
            self.logger.info(f"Device Used: {stats.get('device', 'unknown')}")
        except Exception as e:
            self.logger.error(f"Error getting final statistics: {e}")

def main():
    """Entry point of the application"""
    app = YOLOApplication()
    app.run()

if __name__ == '__main__':
    main()