import time
from kubernetes import client, config

# Load kubeconfig (from ~/.kube/config)
config.load_kube_config()

v1 = client.CoreV1Api()

def check_pods():
    pods = v1.list_pod_for_all_namespaces(watch=False)

    for pod in pods.items:
        name = pod.metadata.name
        namespace = pod.metadata.namespace

        # Check container status
        if pod.status.container_statuses:
            for container in pod.status.container_statuses:

                # Check waiting state (CrashLoopBackOff, Error)
                if container.state.waiting:
                    reason = container.state.waiting.reason

                    if reason in ["CrashLoopBackOff", "Error"]:
                        print("===================================")
                        print(f"🚨 Pod Failure Detected!")
                        print(f"Pod: {name}")
                        print(f"Namespace: {namespace}")
                        print(f"Reason: {reason}")
                        print("===================================")

def main():
    print("Starting Kubernetes Watcher...")
    while True:
        check_pods()
        time.sleep(5)

if __name__ == "__main__":
    main()