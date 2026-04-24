# 🚀 Self-Healing Kubernetes Deployment System

## 📌 Introduction
Modern cloud-native applications deployed on Kubernetes often face issues like pod crashes, service failures, and unexpected downtime. These failures require manual intervention, increasing downtime and operational overhead.

This project introduces a **Self-Healing Kubernetes Deployment System** that automatically:
- Detects failures
- Analyzes root causes
- Takes corrective actions without human intervention

It follows core **SRE (Site Reliability Engineering)** principles:
- Automation
- Observability
- Reliability
- Incident Response

---

## ⚠️ Problem Statement
In real-world environments:
- Pods frequently enter `CrashLoopBackOff`
- Engineers manually check logs
- Restarting or rollback takes time
- No centralized failure tracking

### Challenges:
- Delayed recovery
- Human dependency
- Lack of intelligent decision-making
- No failure history

---

## 🎯 Objectives
- Automatically detect pod failures
- Analyze logs to identify root causes
- Perform automatic recovery (restart/rollback)
- Track failures using metrics
- Provide a visual dashboard

---

## 🏗️ System Architecture

```
User → Kubernetes Cluster → Watcher → Log Analyzer → Healer → Metrics → Dashboard
```

📌 As shown in the architecture diagram (*page 2*), the system consists of:
- Kubernetes Cluster (Kind)
- Watcher (Failure Detection)
- Log Analyzer (Root Cause Detection)
- Healer (Decision Engine)
- Metrics Storage
- Dashboard (Flask UI)

---

## 🛠️ Technology Stack

| Component           | Technology                  |
|--------------------|---------------------------|
| Containerization   | Docker                    |
| Orchestration      | Kubernetes (Kind)         |
| Backend Automation | Python                    |
| Monitoring Logic   | Kubernetes Python Client  |
| Dashboard          | Flask                     |
| Data Storage       | JSON (`metrics.json`)     |

---

## ⚙️ Project Implementation (Phases)

### 🔹 Phase 1 — Application Deployment
- Containerize Node.js app using Docker
- Deploy into Kubernetes
- App intentionally crashes to simulate failures

```bash
kubectl get pods
```

Expected Output:
- Pod status = `CrashLoopBackOff`

---

### 🔹 Phase 2 — Failure Detection (Watcher)
- Python script monitors Kubernetes pods using API

#### Detects:
- CrashLoopBackOff
- Error states

Example Output:
```
🚨 Pod Failure Detected!
Pod: crash-app-xxxxx
```

---

### 🔹 Phase 3 — Log Analysis
- Fetch logs automatically
- Identify root cause patterns

#### Example Detections:
- Application crash
- Memory issues
- Port conflicts

Example Output:
```
Root Cause Analysis:
Intentional Crash
```

---

### 🔹 Phase 4 — Self-Healing Mechanism
- System takes automatic corrective action

#### Actions:
- Restart Pod
- Rollback Deployment (if repeated failures)

---

### 🔹 Phase 5 — Metrics Tracking
- Failures stored in `metrics.json`

#### Stored Data:
- Timestamp
- Pod name
- Namespace
- Failure reason
- Analysis result

---

### 🔹 Phase 6 — Dashboard Visualization
- Flask-based dashboard

#### Features:
- Real-time updates
- Failure history
- Clean UI

Access:
```
http://<IP>:5000
```

📌 Dashboard shown in *page 7* displays failure metrics in tabular format.

---

## 🔄 Working Flow

1. Pod crashes  
2. Watcher detects failure  
3. Logs are fetched  
4. Root cause analyzed  
5. Metrics recorded  
6. Decision engine triggers action  
7. Pod restarted / deployment rolled back  
8. Dashboard updated  

---

## 🚀 Implementation Steps (Execution Guide)

### 1️⃣ Project Setup
```bash
cd ~/self-healing-kubernetes-deployment-system
```

---

### 2️⃣ Environment Setup
```bash
sudo apt update
sudo apt install -y docker.io python3 python3-venv python3-pip curl
sudo systemctl start docker
sudo systemctl enable docker
```

---

### 3️⃣ Install Kubernetes Tools

#### Install Kind
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/
```

#### Install kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

---

### 4️⃣ Cluster Setup
```bash
kind create cluster --name self-healing-cluster
kubectl get nodes
```

---

### 5️⃣ Application Deployment
```bash
cd app
docker build -t crash-app .
cd ..
kind load docker-image crash-app --name self-healing-cluster

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods
```

---

### 6️⃣ Automation Setup
```bash
cd automation
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install kubernetes
```

---

### 7️⃣ Kubernetes Config
```bash
export KUBECONFIG=$HOME/.kube/config
```

---

### 8️⃣ Metrics Initialization
```bash
touch metrics.json
echo "[]" > metrics.json
```

---

### 9️⃣ Run System
```bash
python3 watcher.py
```

---

### 🔟 Verify Metrics
```bash
cat metrics.json
```

---

### 1️⃣1️⃣ Dashboard Setup
```bash
pip install flask
cd ../dashboard
python3 app.py
```

Access:
```
http://<EC2-PUBLIC-IP>:5000
```

---

### 🖥️ Multi-Terminal Execution

**Terminal 1 — Watcher**
```bash
cd automation
source venv/bin/activate
python3 watcher.py
```

**Terminal 2 — Metrics**
```bash
cd automation
cat metrics.json
```

**Terminal 3 — Dashboard**
```bash
cd dashboard
python3 app.py
```

---

## ✨ Key Features
- Automated failure detection
- Intelligent log analysis
- Self-healing capability
- Failure tracking
- Real-time dashboard

---

## ✅ Advantages
- Reduces manual intervention
- Faster recovery time
- Improved reliability
- Demonstrates SRE practices
- Scalable design

---

## ⚠️ Limitations
- Basic log pattern matching
- JSON-based storage (not scalable)
- No authentication in dashboard
- Runs on local cluster (Kind)

---

## 🔮 Future Enhancements
- Integrate Prometheus + Grafana
- Use database (MongoDB / DynamoDB)
- AI-based log analysis
- Deploy watcher inside Kubernetes
- Add alerting (Slack / Email)

---

## 🧠 Conclusion
This project demonstrates a complete **self-healing infrastructure system** using Kubernetes and Python.

It showcases:
- Automation
- Observability
- Intelligent recovery

Aligned with real-world **SRE practices**, it serves as a strong foundation for production-grade DevOps systems.

---

## 🙏 Acknowledgment
This project was developed with the help of:
- Technical documentation
- DevOps learning resources
- AI-assisted tools for concept clarity and debugging

All implementation, integration, and testing were independently executed.

---
