# Start with NVIDIA CUDA base image
FROM nvidia/cuda:12.0.0-base-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,video,utility,graphics \
    PATH="/usr/local/cuda/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}" \
    CUDA_HOME="/usr/local/cuda" \
    PYTHONPATH="${PYTHONPATH}:/workspace" \
    # CUDA optimization
    CUDA_CACHE_MAXSIZE=2147483647 \
    CUDA_CACHE_DISABLE=0 \
    CUDA_FORCE_PTX_JIT=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxrender1 \
    htop \
    iotop \
    nvidia-utils-525 \
    cmake \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    ultralytics \
    torch \
    torchvision \
    opencv-python \
    numpy \
    pandas \
    supervision \
    py-cpuinfo \
    psutil \
    gputil \
    plotly \
    seaborn \
    pillow \
    memory_profiler \
    line_profiler \
    tensorboard \
    pycocotools

# Install monitoring and profiling tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    linux-tools-generic \
    linux-tools-common \
    nvidia-container-toolkit \
    nvidia-cuda-toolkit \
    cuda-command-line-tools-12-0 \
    nsight-systems-2023.2 \
    && rm -rf /var/lib/apt/lists/*

# Create workspace structure
RUN mkdir -p /workspace/app \
    /workspace/data \
    /workspace/models \
    /workspace/results \
    /workspace/logs \
    /workspace/configs

# Set working directory
WORKDIR /workspace

# Download YOLOv8 models
RUN wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -P /workspace/models/ && \
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt -P /workspace/models/ && \
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt -P /workspace/models/

# Copy application code
COPY app/ /workspace/app/
COPY configs/ /workspace/configs/

# Make scripts executable
RUN chmod +x /workspace/app/*.py

# Default command
CMD ["python3", "app/main.py"]