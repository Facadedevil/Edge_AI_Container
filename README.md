# YOLOv8 Real-time Detection System

A comprehensive real-time object detection system using YOLOv8 with performance monitoring and visualization.

## Project Structure
```
yolo-realtime/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── app/
│   ├── main.py                 # Main application entry point
│   ├── realtime_detector.py    # Real-time detection implementation
│   ├── benchmark_utils.py      # Benchmarking utilities
│   ├── monitoring_service.py   # Performance monitoring service
│   ├── visualization_service.py # Real-time visualization dashboard
│   └── utils/
│       ├── __init__.py
│       ├── performance.py      # Performance monitoring utilities
│       └── visualization.py    # Visualization utilities
├── configs/
│   ├── detector_config.yaml    # Detection configuration
│   └── monitoring_config.yaml  # Monitoring configuration
├── data/
│   └── test_images/           # Test images for benchmarking
├── models/                     # YOLOv8 model files
├── results/                    # Results and metrics
└── logs/                      # Application logs
```

## Features
- Real-time object detection using YOLOv8
- Performance monitoring and benchmarking
- Real-time visualization dashboard
- Docker containerization
- GPU optimization
- Comprehensive logging

## Requirements
- NVIDIA GPU with CUDA support
- Docker and Docker Compose
- NVIDIA Container Toolkit

## Installation
1. Clone the repository
```bash
git clone <repository-url>
cd yolo-realtime
```

2. Build and run with Docker Compose
```bash
docker compose up --build
```

## Usage
1. Start the system:
```bash
# Basic usage
python app/main.py

# With custom configuration
python app/main.py --config configs/detector_config.yaml

# With monitoring enabled
python app/main.py --enable-monitoring
```

2. Access the dashboard:
- Open browser and navigate to `http://localhost:8050`

## Configuration
- Edit `configs/detector_config.yaml` for detection settings
- Edit `configs/monitoring_config.yaml` for monitoring settings

## Monitoring and Visualization
- Real-time FPS monitoring
- GPU utilization tracking
- Memory usage monitoring
- Temperature monitoring
- Performance benchmarking

## License
[Specify your license]

## Contributors
Samir Singh