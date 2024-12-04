from kubernetes import client, config
from kubernetes.client.rest import ApiException

def check_pod_status(namespace, pod_name):
    try:
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        status = pod.status.phase
        return status
    except ApiException as e:
        print(f"Exception when checking pod status: {e}")
        return None

def restart_pod(namespace, pod_name):
    try:
        v1 = client.CoreV1Api()
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"Pod {pod_name} restarted successfully.")
    except ApiException as e:
        print(f"Exception when restarting pod: {e}")

def main():
    # Load Kubernetes config from local kubeconfig file
    config.load_kube_config()

    namespace = 'default'
    pod_name = 'your-pod-name'
    
    status = check_pod_status(namespace, pod_name)
    if status != 'Running':
        print(f"Pod {pod_name} is unhealthy. Restarting...")
        restart_pod(namespace, pod_name)
    else:
        print(f"Pod {pod_name} is running fine.")

# Run the monitoring script
main()
