#!/bin/bash

echo "🚀 Starting Project Setup..."

# Update system
sudo apt update

# Install dependencies
sudo apt install -y python3 python3-venv python3-pip docker.io curl

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install kind (if not exists)
if ! command -v kind &> /dev/null
then
    echo "Installing Kind..."
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
fi

# Install kubectl (if not exists)
if ! command -v kubectl &> /dev/null
then
    echo "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
fi

# Create Kubernetes cluster
echo "Creating Kubernetes cluster..."
kind create cluster --name self-healing-cluster

# Build Docker image
echo "Building Docker image..."
cd app
docker build -t crash-app .
cd ..

# Load image into kind
kind load docker-image crash-app --name self-healing-cluster

# Deploy Kubernetes resources
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Setup Python environment
cd automation
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install kubernetes flask

# Initialize metrics file
echo "[]" > metrics.json

cd ..

echo "✅ Setup Complete!"