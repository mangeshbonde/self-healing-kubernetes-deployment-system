#!/bin/bash

echo "🚀 Setting up Self-Healing Kubernetes System..."

# Update system
sudo apt update -y

# Install dependencies
sudo apt install -y python3 python3-venv python3-pip docker.io curl

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install kind
if ! command -v kind &> /dev/null
then
    echo "Installing kind..."
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
fi

# Install kubectl
if ! command -v kubectl &> /dev/null
then
    echo "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
fi

# Create cluster (only if not exists)
if ! kind get clusters | grep -q "self-healing-cluster"
then
    echo "Creating Kubernetes cluster..."
    kind create cluster --name self-healing-cluster
fi

# Build Docker image
echo "Building Docker image..."
cd app
docker build -t crash-app .
cd ..

# Load image into kind
kind load docker-image crash-app --name self-healing-cluster

# Deploy app
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Setup Python environment
cd automation

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r ../requirements.txt

# Initialize metrics file safely
if [ ! -f "metrics.json" ]; then
    echo "[]" > metrics.json
fi

cd ..

echo "✅ Setup completed successfully!"