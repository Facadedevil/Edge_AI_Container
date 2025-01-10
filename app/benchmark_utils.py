# benchmark_utils.py

import time
import torch
import numpy as np
import json
from pathlib import Path
import logging
from contextlib import contextmanager

logger = logging.getLogger('YOLOv8-Benchmark')

class BenchmarkUtils:
    def __init__(self, save_dir='/workspace/results/benchmarks'):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            'inference_times': [],
            'batch_processing_times': [],
            'memory_usage': [],
            'gpu_utilization': []
        }

    @contextmanager
    def timing(self):
        """Context manager for timing operations"""
        start = time.perf_counter()
        yield
        end = time.perf_counter()
        return end - start

    def benchmark_inference(self, model, input_size=(640, 640), batch_sizes=[1, 2, 4, 8], iterations=100):
        """Benchmark inference performance"""
        results = {}
        
        for batch_size in batch_sizes:
            times = []
            memory_usage = []
            
            # Create dummy input
            dummy_input = torch.randn(batch_size, 3, *input_size).cuda()
            
            # Warmup
            for _ in range(10):
                _ = model(dummy_input)
            
            # Benchmark
            torch.cuda.synchronize()
            for _ in range(iterations):
                torch.cuda.reset_peak_memory_stats()
                
                start = time.perf_counter()
                _ = model(dummy_input)
                torch.cuda.synchronize()
                end = time.perf_counter()
                
                times.append(end - start)
                memory_usage.append(torch.cuda.max_memory_allocated() / 1024**2)  # MB
            
            results[batch_size] = {
                'mean_time': np.mean(times),
                'std_time': np.std(times),
                'min_time': np.min(times),
                'max_time': np.max(times),
                'mean_memory': np.mean(memory_usage),
                'fps': batch_size / np.mean(times)
            }
        
        return results

    def benchmark_throughput(self, model, input_size=(640, 640), duration=60):
        """Benchmark maximum throughput"""
        batch_size = 1
        frames_processed = 0
        start_time = time.time()
        
        dummy_input = torch.randn(batch_size, 3, *input_size).cuda()
        
        while (time.time() - start_time) < duration:
            _ = model(dummy_input)
            torch.cuda.synchronize()
            frames_processed += batch_size
        
        total_time = time.time() - start_time
        throughput = frames_processed / total_time
        
        return {
            'frames_processed': frames_processed,
            'total_time': total_time,
            'throughput': throughput
        }

    def profile_memory(self, model, input_size=(640, 640), batch_size=1):
        """Profile memory usage"""
        dummy_input = torch.randn(batch_size, 3, *input_size).cuda()
        
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
        
        # Initial memory
        init_memory = torch.cuda.memory_allocated()
        
        # Run inference
        _ = model(dummy_input)
        torch.cuda.synchronize()
        
        # Peak memory
        peak_memory = torch.cuda.max_memory_allocated()
        
        return {
            'initial_memory': init_memory / 1024**2,  # MB
            'peak_memory': peak_memory / 1024**2,
            'memory_increase': (peak_memory - init_memory) / 1024**2
        }

    def save_results(self, results, name='benchmark_results'):
        """Save benchmark results to file"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        result_file = self.save_dir / f'{name}_{timestamp}.json'
        
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"Benchmark results saved to {result_file}")

    def run_comprehensive_benchmark(self, model, input_sizes=[(640, 640), (1280, 1280)]):
        """Run comprehensive benchmark suite"""
        results = {
            'model_info': {
                'name': model.__class__.__name__,
                'device': next(model.parameters()).device.type
            },
            'benchmarks': {}
        }
        
        for input_size in input_sizes:
            size_str = f"{input_size[0]}x{input_size[1]}"
            results['benchmarks'][size_str] = {
                'inference': self.benchmark_inference(model, input_size),
                'throughput': self.benchmark_throughput(model, input_size),
                'memory': self.profile_memory(model, input_size)
            }
        
        self.save_results(results)
        return results