# Containerized Media Uploader for MicroK8s

A lightweight, containerized Python Flask web application that accepts web images or videos and saves them to cluster-backed persistent storage. This repository serves as an educational exercise for building custom Docker images, utilizing local registries, and implementing Kubernetes persistent storage.

## 🚀 Features
* **Media Uploads**: Accepts `.jpg`, `.png`, `.gif`, `.mp4`, and `.webm` file formats (Max 50MB).
* **Containerized Architecture**: Packaged into a minimal Docker container using `python:3.11-slim`.
* **Persistent Storage**: Utilizes a Kubernetes `PersistentVolumeClaim` (PVC) mapped to a MicroK8s `hostpath-storage` provisioner to ensure data survives pod restarts.
* **Local Registry Integration**: Configured to build, push, and deploy seamlessly using the MicroK8s built-in registry.

## 🛠️ Prerequisites & Cluster Setup

Ensure your local Linux workstation or VM has at least 2 vCPUs, 4 GB RAM, and Docker Engine installed. 

1. **Install MicroK8s:**
   ```bash
   sudo snap install microk8s --classic
   ```

2. **Enable Required Addons:**
   ```bash
   # Enable dynamic storage provisioning
   microk8s enable hostpath-storage

   # Enable local container registry at localhost:32000
   microk8s enable registry
   ```

## 📦 How to Build and Deploy

### 1. Build and Push the Container Image
Navigate to your project directory and build your image tagged for the local MicroK8s registry:
```bash
# Build the container image
docker build -t localhost:32000/media-uploader:v6 .

# Push the image to the local cluster registry
docker push localhost:32000/media-uploader:v6
```

### 2. Apply Kubernetes Manifests
Deploy the storage backend, application layer, and network service to your cluster:
```bash
# Deploy persistent volume claim
microk8s kubectl apply -f storage.yaml

# Deploy application deployment and NodePort service
microk8s kubectl apply -f deployment.yaml
```

### 3. Access the Application
Verify that your pods are up and running:
```bash
microk8s kubectl get pods -l app=media-uploader
```
Open your web browser and navigate to: `http://localhost:30080` (or your Node's IP address).

## 🧪 Verifying Data Persistence

To test that data persists independently of the application lifecycle:
1. Upload an image or video through the web UI.
2. Force delete the running pod to trigger a replacement:
   ```bash
   microk8s kubectl delete pod -l app=media-uploader
   ```
3. Wait for the deployment to initialize a new pod (`microk8s kubectl get pods -w`).
4. Refresh your browser at `http://localhost:30080`. Your uploaded files will remain safely accessible.
