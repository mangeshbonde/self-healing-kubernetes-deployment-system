import time
from kubernetes import client, config
from log_analyzer import analyze_pod
from healer import decide_and_heal

# Load kubeconfig
config.load_kube_config()

v1 = client.CoreV1Api()

def check_pods():
    pods = v1.list_pod_for_all_namespaces(watch=False)

    for pod in pods.items:
        name = pod.metadata.name
        namespace = pod.metadata.namespace

        if pod.status.container_statuses:
            for container in pod.status.container_statuses:

                if container.state.waiting:
                    reason = container.state.waiting.reason

                    if reason in ["CrashLoopBackOff", "Error"]:
                        print("\n===================================")
                        print(f"🚨 Pod Failure Detected!")
                        print(f"Pod: {name}")
                        print(f"Namespace: {namespace}")
                        print(f"Reason: {reason}")

                        # Analyze
                        result = analyze_pod(name, namespace)

                        # Heal
                        decide_and_heal(name, namespace, result)

                        print("===================================")

def main():
    print("Starting Self-Healing Kubernetes System...")
    while True:
        check_pods()
        time.sleep(5)

if __name__ == "__main__":
    main()