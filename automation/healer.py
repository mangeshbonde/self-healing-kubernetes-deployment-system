from kubernetes import client, config
import os

# Load config
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
    print("\n🧠 Decision Engine Running...")

    # Extract deployment name (basic logic)
    deployment_name = pod_name.split('-')[0]

    if "Intentional Crash" in analysis_result:
        restart_pod(pod_name, namespace)

    elif "Memory Issue" in analysis_result:
        print("⚠️ Memory issue detected → Restarting pod")
        restart_pod(pod_name, namespace)

    elif "Application Error" in analysis_result:
        print("⚠️ Application bug → Rolling back deployment")
        rollback_deployment(deployment_name, namespace)

    else:
        print("⚠️ Unknown issue → Restarting pod as fallback")
        restart_pod(pod_name, namespace)