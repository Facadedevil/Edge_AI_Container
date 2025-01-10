#!/usr/bin/env python3
# realtime_detector.py

import cv2
import torch
import supervision as sv
import numpy as np
import time
from collections import deque
import threading
from queue import Queue
from ultralytics import YOLO
import logging
from utils.performance import PerformanceMonitor

logger = logging.getLogger('YOLOv8-Realtime')

class RealtimeObjectDetector:
    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.3, buffer_size=30):
        """
        Initialize real-time detector with performance monitoring
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {self.device}")
        
        # Load model
        try:
            self.model = YOLO(model_path)
            logger.info(f"Model loaded successfully: {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
        
        self.conf_threshold = conf_threshold
        self.performance_monitor = PerformanceMonitor(buffer_size)
        
        # Initialize queues for frame processing
        self.frame_queue = Queue(maxsize=buffer_size)
        self.result_queue = Queue(maxsize=buffer_size)
        
        # Initialize annotators
        self.box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )
        
        # Initialize object tracker
        self.tracker = sv.ByteTrack()
        self.trace_annotator = sv.TraceAnnotator(
            thickness=2,
            trace_length=15
        )

    def start_processing_thread(self):
        """Start the background processing thread"""
        self.processing_thread = threading.Thread(
            target=self._process_frames_thread,
            daemon=True
        )
        self.processing_thread.start()

    def _process_frames_thread(self):
        """Background thread for frame processing"""
        while True:
            frame = self.frame_queue.get()
            if frame is None:
                break
            
            try:
                # Process frame with performance monitoring
                with self.performance_monitor.measure_processing_time():
                    # Run inference
                    results = self.model(frame, conf=self.conf_threshold)[0]
                    detections = sv.Detections.from_yolov8(results)
                    
                    # Update tracks
                    detections = self.tracker.update_with_detections(detections)
                
                self.result_queue.put((frame, detections))
            except Exception as e:
                logger.error(f"Error processing frame: {e}")
                continue

    def process_camera(self, source=0, display_stats=True):
        """Process camera feed with real-time statistics"""
        logger.info(f"Starting camera processing from source: {source}")
        
        # Start processing thread
        self.start_processing_thread()
        
        try:
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                raise ValueError(f"Error opening camera {source}")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Add frame to processing queue if not full
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
                
                # Get and display processed results
                if not self.result_queue.empty():
                    self._display_processed_frame(
                        *self.result_queue.get(),
                        display_stats=display_stats
                    )
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        except Exception as e:
            logger.error(f"Error in camera processing: {e}")
        finally:
            self._cleanup()

    def _display_processed_frame(self, frame, detections, display_stats=True):
        """Display processed frame with annotations and stats"""
        # Create labels for detected objects
        labels = [
            f"{self.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        
        # Draw detections and traces
        frame = self.trace_annotator.annotate(frame, detections)
        frame = self.box_annotator.annotate(frame, detections, labels)
        
        # Add performance stats overlay
        if display_stats:
            stats = self.get_performance_stats()
            self._add_stats_overlay(frame, stats, len(detections))
        
        cv2.imshow('YOLOv8 Real-time Detection', frame)

    def _add_stats_overlay(self, frame, stats, num_objects):
        """Add performance statistics overlay to frame"""
        stats_text = (
            f"FPS: {stats['fps']:.1f} | "
            f"Processing Time: {stats['processing_time']*1000:.1f}ms | "
            f"Objects: {num_objects} | "
            f"Device: {self.device}"
        )
        
        cv2.putText(
            frame,
            stats_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    def _cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        self.frame_queue.put(None)
        if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
            self.processing_thread.join()
        cv2.destroyAllWindows()

    def get_performance_stats(self):
        """Get current performance statistics"""
        return self.performance_monitor.get_stats()