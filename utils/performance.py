#!/usr/bin/env python3
# utils/performance.py

import time
from collections import deque
import numpy as np
import psutil
import GPUtil
from contextlib import contextmanager
import logging

logger = logging.getLogger('YOLOv8-Performance')

class PerformanceMonitor:
    def __init__(self, buffer_size=30):
        """Initialize performance monitoring"""
        self.buffer_size = buffer_size
        self.fps_buffer = deque(maxlen=buffer_size)
        self.processing_times = deque(maxlen=buffer_size)
        self.last_fps_update = time.time()
        self.frames_processed = 0

    @contextmanager
    def measure_processing_time(self):
        """Context manager to measure processing time"""
        start_time = time.perf_counter()
        try:
            yield
        finally:
            process_time = time.perf_counter() - start_time
            self.processing_times.append(process_time)
            self._update_fps()

    def _update_fps(self):
        """Update FPS calculation"""
        self.frames_processed += 1
        current_time = time.time()
        time_diff = current_time - self.last_fps_update

        if time_diff >= 1.0:
            fps = self.frames_processed / time_diff
            self.fps_buffer.append(fps)
            self.frames_processed = 0
            self.last_fps_update = current_time

    def get_gpu_stats(self):
        """Get GPU statistics"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Get primary GPU
                return {
                    'gpu_load': gpu.load * 100,
                    'gpu_memory_used': gpu.memoryUsed,
                    'gpu_memory_total': gpu.memoryTotal,
                    'gpu_temperature': gpu.temperature
                }
        except Exception as e:
            logger.error(f"Error getting GPU stats: {e}")
        return {}

    def get_system_stats(self):
        """Get system statistics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available': psutil.virtual_memory().available / (1024 ** 2)  # MB
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
        return {}

    def get_stats(self):
        """Get comprehensive performance statistics"""
        stats = {
            'fps': np.mean(self.fps_buffer) if self.fps_buffer else 0,
            'processing_time': np.mean(self.processing_times) if self.processing_times else 0,
            'processing_time_std': np.std(self.processing_times) if self.processing_times else 0
        }
        
        # Add GPU and system stats
        stats.update(self.get_gpu_stats())
        stats.update(self.get_system_stats())
        
        return stats

    def log_performance(self):
        """Log current performance metrics"""
        stats = self.get_stats()
        logger.info(
            f"Performance Metrics - "
            f"FPS: {stats['fps']:.1f}, "
            f"Processing Time: {stats['processing_time']*1000:.1f}ms, "
            f"GPU Load: {stats.get('gpu_load', 'N/A')}%, "
            f"GPU Memory: {stats.get('gpu_memory_used', 'N/A')}/{stats.get('gpu_memory_total', 'N/A')}MB"
        )