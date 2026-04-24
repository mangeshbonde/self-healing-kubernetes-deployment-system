from kubernetes import client, config
import os
from metrics import count_recent_failures

# Load Kubernetes config
config.load_kube_config()

apps_v1 = client.AppsV1Api()
v1 = client.CoreV1Api()

def restart_pod(pod_name, namespace="default"):
    print("🔄 Restarting pod...")

    try:
        v1.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )
        print(f"✅ Pod {pod_name} deleted (will restart automatically)")
    except Exception as e:
        print(f"❌ Error restarting pod: {e}")


def rollback_deployment(deployment_name, namespace="default"):
    print("⏪ Rolling back deployment...")

    try:
        command = f"kubectl rollout undo deployment {deployment_name} -n {namespace}"
        os.system(command)
        print(f"✅ Rollback triggered for {deployment_name}")
    except Exception as e:
        print(f"❌ Rollback failed: {e}")


def decide_and_heal(pod_name, namespace, analysis_result):
    print("\n🧠 Smart Decision Engine Running...")

    deployment_name = pod_name.split('-')[0]

    failure_count = count_recent_failures(pod_name)

    print(f"📊 Recent failures: {failure_count}")

    if failure_count >= 3:
        print("⚠️ Too many failures → Rolling back deployment")
        rollback_deployment(deployment_name, namespace)

    elif "Intentional Crash" in analysis_result:
        restart_pod(pod_name, namespace)

    elif "Memory Issue" in analysis_result:
        restart_pod(pod_name, namespace)

    elif "Application Error" in analysis_result:
        rollback_deployment(deployment_name, namespace)

    else:
        print("⚠️ Unknown issue → Restarting pod")
        restart_pod(pod_name, namespace)