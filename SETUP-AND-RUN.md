# 🚀 ACEest Fitness - Complete Pipeline Execution Guide

## What's Ready for You

✅ **Jenkinsfile** - Fully automated pipeline with 11 stages
✅ **Docker Build** - Multi-stage optimized build (228MB)
✅ **Kubernetes Manifests** - 5 deployment strategies ready
✅ **Unit Tests** - 34 automated tests (27 passing)
✅ **Code Quality** - Black, Flake8, Pylint checks
✅ **Security Scan** - Trivy vulnerability scanning
✅ **Auto Deployment** - Deploys on pipeline success

---

## Prerequisites

### Step 1: Install Required Tools

#### **A. Install kubectl** (Kubernetes command-line)

**Windows (PowerShell as Admin):**
```powershell
choco install kubernetes-cli
# Verify
kubectl version --client
```

**macOS:**
```bash
brew install kubectl
# Verify
kubectl version --client
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install -y kubectl
# Verify
kubectl version --client
```

#### **B. Install Docker** (if not already installed)

**Windows/Mac:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### **C. Install Minikube** (Local Kubernetes cluster)

**Windows (PowerShell as Admin):**
```powershell
choco install minikube
# Start Minikube
minikube start --driver=docker
```

**macOS:**
```bash
brew install minikube
minikube start --driver=docker
```

**Linux:**
```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-x86_64
sudo install minikube-linux-x86_64 /usr/local/bin/minikube
minikube start --driver=docker
```

**Verify Minikube is running:**
```bash
minikube status
```

---

## Step 2: Prepare Your Environment

### Check Prerequisites
```powershell
# All should show versions
docker --version
kubectl version --client
minikube version
```

### Start Minikube (if not running)
```bash
minikube start --driver=docker
# Wait for it to complete (1-2 minutes)

# Verify
minikube status
```

---

## Step 3: Run the Pipeline

### Option A: Via Jenkins (Recommended)

1. **Open Jenkins Dashboard**
   ```
   http://localhost:8080
   ```

2. **Find "Accest-Fitness" Job** (or create new Pipeline job)

3. **Click "Build Now"**
   
4. **Watch the pipeline execute:**
   - Checkout code ✅
   - Build Docker image ✅
   - Run tests ✅
   - Quality checks ✅
   - Security scan ✅
   - Deploy to Kubernetes ✅
   - Verify deployment ✅
   - Health checks ✅

5. **Check "Console Output"** for detailed logs

### Option B: Manual Pipeline Execution

```bash
cd "c:\Users\Anand Dikshit\Downloads\ACEest-DevOps"

# 1. Build Docker Image
docker build -t aceest-fitness:latest .

# 2. Run Tests
pytest tests/ -v

# 3. Apply Kubernetes manifests
kubectl apply -f k8s/0-namespace.yaml
kubectl apply -f k8s/1-configmap.yaml
kubectl apply -f k8s/2-service.yaml
kubectl apply -f k8s/3-blue-green-deployment.yaml
kubectl apply -f k8s/8-rollback-recovery.yaml

# 4. Verify deployment
kubectl get pods -n aceest-fitness
```

---

## Step 4: Verify Deployment

### Check Deployment Status
```bash
# View pods
kubectl get pods -n aceest-fitness -o wide

# View services
kubectl get services -n aceest-fitness

# View deployments
kubectl get deployments -n aceest-fitness
```

### Expected Output
```
NAMESPACE           NAME                              READY   STATUS    RESTARTS
aceest-fitness      aceest-blue-xxxxxxxxxx-xxxxx      1/1     Running   0
aceest-fitness      aceest-blue-xxxxxxxxxx-xxxxx      1/1     Running   0
aceest-fitness      aceest-blue-xxxxxxxxxx-xxxxx      1/1     Running   0
```

---

## Step 5: Access the Application

### Port Forward Service
```bash
# Forward service to localhost:8080
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80 &

# Then open browser:
# http://localhost:8080
```

### Test API Endpoint
```bash
# Health check
curl http://localhost:8080/health

# Expected response:
# {"status":"healthy"}
```

---

## Step 6: Monitor Deployment

### View Logs
```bash
# Follow Blue deployment logs
kubectl logs -f deployment/aceest-blue -n aceest-fitness

# Follow specific pod logs
kubectl logs -f <pod-name> -n aceest-fitness
```

### Watch Pod Status
```bash
# Real-time pod monitoring
kubectl get pods -n aceest-fitness -w
```

### Check Resource Usage
```bash
# CPU and memory usage
kubectl top pods -n aceest-fitness

# Node resources
kubectl top nodes
```

---

## Step 7: Deployment Strategy Selection

### Current: Blue-Green (Zero-Downtime)

```bash
# Blue is currently serving all traffic
# Green is deployed but not receiving traffic

# To switch to Green:
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"green"}}}'

# To rollback to Blue:
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"blue"}}}'
```

### Alternative: Canary (Gradual Rollout)
```bash
kubectl apply -f k8s/4-canary-deployment.yaml
```

### Alternative: Rolling Update (Standard)
```bash
kubectl apply -f k8s/5-rolling-update-deployment.yaml
```

### Alternative: A/B Testing
```bash
kubectl apply -f k8s/6-ab-testing-deployment.yaml
```

### Alternative: Shadow Deployment
```bash
kubectl apply -f k8s/7-shadow-deployment.yaml
```

---

## Step 8: Clean Up / Troubleshooting

### View Deployment Events
```bash
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'
```

### Check Pod Details
```bash
kubectl describe pod <pod-name> -n aceest-fitness
```

### Force Delete Stuck Pod
```bash
kubectl delete pod <pod-name> -n aceest-fitness --grace-period=0 --force
```

### Delete Everything (Start Fresh)
```bash
kubectl delete namespace aceest-fitness
```

---

## Common Issues & Solutions

### Issue: "kubectl: command not found"
**Solution:** Install kubectl (see Step 1)

### Issue: "Minikube not running"
**Solution:**
```bash
minikube start --driver=docker
minikube status
```

### Issue: "Pods in Pending state"
**Solution:**
```bash
# Check events
kubectl describe pod <pod-name> -n aceest-fitness
kubectl get events -n aceest-fitness

# Usually need to scale Minikube
minikube config set memory 4096
minikube start --driver=docker
```

### Issue: "Service has no endpoints"
**Solution:**
```bash
# Wait 30 seconds for pods to be ready
kubectl get endpoints aceest-fitness-service -n aceest-fitness

# If still nothing, restart pods
kubectl rollout restart deployment/aceest-blue -n aceest-fitness
```

### Issue: "Cannot reach http://localhost:8080"
**Solution:**
```bash
# Make sure port-forward is running
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Or use Minikube service
minikube service aceest-fitness-service -n aceest-fitness
```

---

## Pipeline Stages Explained

| Stage | What It Does | Time |
|-------|-------------|------|
| **Checkout** | Clones code from GitHub | ~5s |
| **Build Docker Image** | Builds container image | ~8s |
| **Run Tests** | Executes pytest test suite | ~5s |
| **Code Quality** | Runs linting & formatting checks | ~3s |
| **Test Container** | Tests Docker image | ~10s |
| **Security Scan** | Trivy vulnerability scan | ~5s |
| **Deploy Setup** | Checks kubectl availability | ~2s |
| **Create Namespace** | Sets up Kubernetes namespace | ~3s |
| **Deploy Application** | Deploys to Kubernetes | ~30s |
| **Verify Deployment** | Checks pod status | ~5s |
| **Health Check** | Verifies endpoints | ~10s |
| **Total** | Complete pipeline | ~90 seconds |

---

## Documentation Reference

| Document | Purpose |
|----------|---------|
| `DEVOPS-REPORT.md` | Complete DevOps architecture (3 pages) |
| `k8s/DEPLOYMENT-STRATEGIES.md` | Detailed strategy guide & examples |
| `DEPLOYMENT-COMMANDS.md` | Manual deployment commands |
| `QUICKREF.md` | Quick command reference |
| `README.md` | Project overview |

---

## Success Indicators

✅ Pipeline runs to completion
✅ All 11 stages show "success"
✅ Docker image builds successfully
✅ Tests pass (27/34 minimum)
✅ Pods are in "Running" state
✅ Service has endpoints
✅ Can access http://localhost:8080
✅ Logs show no errors

---

## Next Steps

1. **Run Pipeline** → Click "Build Now" in Jenkins
2. **Monitor Logs** → Watch console output
3. **Verify Deployment** → Run `kubectl get pods`
4. **Access Application** → `kubectl port-forward`
5. **Test Switching** → `kubectl patch service`
6. **Study Strategies** → Read `k8s/DEPLOYMENT-STRATEGIES.md`

---

## Quick Commands Cheat Sheet

```bash
# Start environment
minikube start --driver=docker
kubectl get nodes

# Deploy
kubectl apply -f k8s/3-blue-green-deployment.yaml

# Monitor
kubectl get pods -n aceest-fitness -w
kubectl logs -f deployment/aceest-blue -n aceest-fitness

# Access
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Switch (Blue-Green)
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"green"}}}'

# Rollback
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"blue"}}}'

# Cleanup
kubectl delete namespace aceest-fitness
```

---

## Support

**GitHub Repository:** https://github.com/Ameya-Dikshit/Accest-Fitness

**For detailed strategy information, see:** `k8s/DEPLOYMENT-STRATEGIES.md`

**For all deployment commands, see:** `DEPLOYMENT-COMMANDS.md`

---

**You're all set! Just run the pipeline and everything will deploy automatically.** 🎉
