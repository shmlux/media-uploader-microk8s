# Media Uploader Application

A containerized Python media application deployed on a local single-node Kubernetes cluster using **MicroK8s**.

## 🛠 Kubernetes Architecture & Ports

The application uses a **NodePort Service** to bridge internal container traffic to the external host environment. 

| Layer | Component / Configuration | Target Port |
| :--- | :--- | :--- |
| **Frontend Access (Mac)** | Web Browser (Host Machine) | `http://<VM_IP>:30080` |
| **Cluster External Layer**| `media-service` (NodePort) | `30080` |
| **Cluster Internal Layer**| `media-service` (ClusterIP)| `80` |
| **Application Layer**     | `app.py` / Container Port | `80` |

> ⚠️ **Important Networking Note:** Because of MicroK8s local network isolation rules, the NodePort cannot be reliably reached over standard host SSH tunnels (`localhost:30080`). Traffic must be port-forwarded across all interfaces.

## 🚀 Deployment & Local Access Instructions

1. **Apply the Kubernetes manifests:**
   ```bash
   sudo microk8s kubectl apply -f storage.yaml
   sudo microk8s kubectl apply -f deployment.yaml
   sudo microk8s kubectl apply -f media-service.yaml
   ```

2. **Expose the service to your host machine (Mac):**
   Run the following port-forward command inside the VM to bind the cluster traffic to all network interfaces:
   ```bash
   sudo microk8s kubectl port-forward --address 0.0.0.0 service/media-service 30080:80
   ```

3. **Open the Application:**
   Find your VM's IP address (`hostname -I`) and open your Mac's browser to:
   `http://<YOUR_VM_IP_ADDRESS>:30080`
