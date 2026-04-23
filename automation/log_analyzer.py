from kubernetes import client, config

# Load Kubernetes config
config.load_kube_config()

v1 = client.CoreV1Api()

def get_pod_logs(pod_name, namespace="default"):
    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=50
        )
        return logs
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return ""

def analyze_logs(logs):
    logs = logs.lower()

    if "error" in logs:
        return "Application Error Detected"

    if "connection refused" in logs:
        return "Service Dependency Failure"

    if "out of memory" in logs:
        return "Memory Issue (OOMKilled)"

    if "port already in use" in logs:
        return "Port Conflict Issue"

    if "simulating crash" in logs:
        return "Intentional Crash (Test Scenario)"

    return "Unknown Issue"

def analyze_pod(pod_name, namespace="default"):
    print("\n📥 Fetching logs...")
    logs = get_pod_logs(pod_name, namespace)

    print("\n📊 Analyzing logs...")
    result = analyze_logs(logs)

    print("===================================")
    print(f"🧠 Root Cause Analysis for {pod_name}")
    print(f"Result: {result}")
    print("===================================")

    return result