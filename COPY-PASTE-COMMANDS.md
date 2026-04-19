# 🚀 DEPLOYMENT COMMANDS - Copy & Paste Ready

## ✅ Everything is Ready - Just Execute These Commands!

---

## STEP 1: Prerequisites (One-Time Setup)

```powershell
# Windows PowerShell (As Administrator)
choco install kubernetes-cli
choco install minikube
choco install docker

# Verify
kubectl version --client
minikube version
docker --version
```

---

## STEP 2: Start Kubernetes Environment

```powershell
# Start Minikube
minikube start --driver=docker

# Verify it's running
minikube status
kubectl get nodes
```

---

## STEP 3: Deploy Application

### 🔴 OPTION A: Full Automated Pipeline (BEST)
```powershell
# In Jenkins UI:
# 1. Go to http://localhost:8080
# 2. Click on "Accest-Fitness" job
# 3. Click "Build Now"
# 4. Watch it deploy automatically!

# Or trigger from command line:
cd "c:\Users\Anand Dikshit\Downloads\ACEest-DevOps"
curl -X POST http://localhost:8080/job/Accest-Fitness/build
```

### 🟢 OPTION B: Manual Kubernetes Deploy
```powershell
cd "c:\Users\Anand Dikshit\Downloads\ACEest-DevOps"

# Deploy all manifests
kubectl apply -f k8s/0-namespace.yaml
kubectl apply -f k8s/1-configmap.yaml
kubectl apply -f k8s/2-service.yaml
kubectl apply -f k8s/3-blue-green-deployment.yaml
kubectl apply -f k8s/8-rollback-recovery.yaml

echo "Deployment complete!"
```

### 🟡 OPTION C: Individual Strategies
```powershell
cd "c:\Users\Anand Dikshit\Downloads\ACEest-DevOps"

# Canary (Gradual rollout)
kubectl apply -f k8s/4-canary-deployment.yaml

# Rolling Update (Standard with auto-scaling)
kubectl apply -f k8s/5-rolling-update-deployment.yaml

# A/B Testing (Feature variants)
kubectl apply -f k8s/6-ab-testing-deployment.yaml

# Shadow (Production testing)
kubectl apply -f k8s/7-shadow-deployment.yaml
```

---

## STEP 4: Verify Deployment

```powershell
# Check pods are running
kubectl get pods -n aceest-fitness -o wide

# Check services
kubectl get services -n aceest-fitness

# Check deployments
kubectl get deployments -n aceest-fitness

# All resources
kubectl get all -n aceest-fitness
```

---

## STEP 5: Access Application

```powershell
# Terminal 1: Port forward
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Terminal 2: Test application
# Open browser: http://localhost:8080

# Or test API
curl http://localhost:8080/health
```

---

## STEP 6: View Logs

```powershell
# Follow Blue deployment logs
kubectl logs -f deployment/aceest-blue -n aceest-fitness

# Follow specific pod
kubectl logs -f pod/<pod-name> -n aceest-fitness

# Watch pods in real-time
kubectl get pods -n aceest-fitness -w
```

---

## STEP 7: Switch Deployments (Blue-Green)

```powershell
# Switch from Blue to Green
kubectl patch service aceest-fitness-service -n aceest-fitness `
  -p '{"spec":{"selector":{"variant":"green"}}}'

# Rollback to Blue
kubectl patch service aceest-fitness-service -n aceest-fitness `
  -p '{"spec":{"selector":{"variant":"blue"}}}'

# Check which variant is active
kubectl get service aceest-fitness-service -n aceest-fitness -o jsonpath='{.spec.selector.variant}'
```

---

## STEP 8: Clean Up

```powershell
# Delete all pods (keeps namespace)
kubectl delete pods --all -n aceest-fitness

# Delete entire namespace (complete cleanup)
kubectl delete namespace aceest-fitness

# Delete Minikube cluster
minikube delete
```

---

## 🎯 Most Common Commands

```powershell
# Quick status check
kubectl get pods -n aceest-fitness

# Quick logs
kubectl logs -f deployment/aceest-blue -n aceest-fitness

# Quick port forward
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Quick rollback (Blue-Green)
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"variant":"blue"}}}'
```

---

## 📊 Pipeline Execution Flow

```
┌─── RUN PIPELINE ────┐
│ (Jenkins or manual) │
└─────────┬───────────┘
          ↓
    ✅ Build Docker
          ↓
    ✅ Run Tests
          ↓
    ✅ Code Quality
          ↓
    ✅ Security Scan
          ↓
    ✅ Deploy to K8s
          ↓
    ✅ Verify Status
          ↓
    ✅ Health Check
          ↓
    🎉 READY TO USE!
```

---

## ✔️ Success Checklist

- [ ] `kubectl get nodes` shows at least 1 node
- [ ] `kubectl get pods -n aceest-fitness` shows pods in Running state
- [ ] `kubectl get services -n aceest-fitness` shows aceest-fitness-service
- [ ] `curl http://localhost:8080/health` returns {"status":"healthy"}
- [ ] Jenkins pipeline shows all 11 stages with ✅ success

---

## 🔧 Troubleshooting Quick Fixes

```powershell
# Pods won't start?
kubectl describe pod <pod-name> -n aceest-fitness

# Service has no endpoints?
kubectl get endpoints aceest-fitness-service -n aceest-fitness

# Deployment stuck?
kubectl rollout status deployment/aceest-blue -n aceest-fitness

# Force restart
kubectl rollout restart deployment/aceest-blue -n aceest-fitness

# Check events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'
```

---

## 📱 Save These Bookmarks

- **Jenkins:** http://localhost:8080
- **Application:** http://localhost:8080 (after port-forward)
- **GitHub:** https://github.com/Ameya-Dikshit/Accest-Fitness
- **Documentation:** See `READY-TO-DEPLOY.md`

---

## ⏱️ Quick Time Reference

| Task | Time |
|------|------|
| Install tools | 10-15 min |
| Start Minikube | 1-2 min |
| Run pipeline | ~90 sec |
| Deploy & verify | 2-3 min |
| **Total first-time** | **20-25 min** |

---

## 🎉 YOU'RE READY!

**Recommended:** Start with **OPTION A** (Jenkins Pipeline) - it's fully automated!

```powershell
# 1. Make sure Minikube is running
minikube status

# 2. Open Jenkins
start http://localhost:8080

# 3. Click "Build Now"

# 4. Watch the magic happen! ✨
```

---

**Status:** ✅ Everything is set up and ready to deploy!

**Next command to run:** 
```powershell
minikube start --driver=docker
```

**Then:**
```powershell
kubectl get nodes
```

**Then open Jenkins and click "Build Now"!** 🚀
