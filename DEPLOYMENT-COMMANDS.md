# ACEest Fitness Deployment Commands

## 🚀 Quick Start - Just Run the Pipeline!

The **Jenkinsfile** is now configured to automatically:
1. ✅ Build Docker image
2. ✅ Run all tests
3. ✅ Check code quality
4. ✅ Scan for security vulnerabilities
5. ✅ Deploy to Kubernetes (Blue-Green strategy)
6. ✅ Verify deployment status

**Just click "Build Now" in Jenkins and the pipeline handles everything!**

---

## 📋 Manual Deployment Commands

### Prerequisites
```bash
# Install kubectl
# macOS: brew install kubectl
# Linux: sudo apt-get install kubectl
# Windows: choco install kubernetes-cli

# Install/start Minikube (local Kubernetes)
minikube start --driver=docker
```

### Deployment Strategies

#### **1. Blue-Green Deployment** (Zero-Downtime)
```bash
# Deploy namespace and config
kubectl apply -f k8s/0-namespace.yaml
kubectl apply -f k8s/1-configmap.yaml
kubectl apply -f k8s/2-service.yaml

# Deploy Blue (stable) + Green (new)
kubectl apply -f k8s/3-blue-green-deployment.yaml

# Verify deployment
kubectl get pods -n aceest-fitness

# Test Blue deployment (currently serving traffic)
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80
# Open: http://localhost:8080

# When ready, scale Green to 3 replicas
kubectl scale deployment aceest-green --replicas=3 -n aceest-fitness

# Switch traffic to Green
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"green"}}}'

# If issues, instantly rollback to Blue
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"blue"}}}'
```

#### **2. Canary Deployment** (Gradual Rollout)
```bash
# Deploy Canary + Stable
kubectl apply -f k8s/4-canary-deployment.yaml

# Monitor metrics
kubectl logs -f deployment/aceest-canary -n aceest-fitness

# Gradually increase canary traffic
kubectl scale deployment aceest-canary --replicas=2 -n aceest-fitness
kubectl scale deployment aceest-canary --replicas=3 -n aceest-fitness

# When stable, scale down stable and canary up
kubectl scale deployment aceest-stable --replicas=0 -n aceest-fitness
```

#### **3. Rolling Update** (Standard + Auto-Scaling)
```bash
# Deploy with automatic scaling
kubectl apply -f k8s/5-rolling-update-deployment.yaml

# Monitor rollout status
kubectl rollout status deployment/aceest-rolling -n aceest-fitness

# Check HPA status
kubectl get hpa -n aceest-fitness

# If issues, auto-rollback via readiness probes
# Manual rollback:
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness

# View deployment history
kubectl rollout history deployment/aceest-rolling -n aceest-fitness
```

#### **4. A/B Testing** (Feature Variants)
```bash
# Deploy Variant A and B
kubectl apply -f k8s/6-ab-testing-deployment.yaml

# View both variants
kubectl get pods -n aceest-fitness -L variant

# Monitor variant A logs
kubectl logs -f deployment/aceest-variant-a -n aceest-fitness

# Monitor variant B logs
kubectl logs -f deployment/aceest-variant-b -n aceest-fitness

# Promote winning variant (scale down loser)
kubectl scale deployment aceest-variant-a --replicas=0 -n aceest-fitness
```

#### **5. Shadow Deployment** (Production Testing)
```bash
# Deploy Production + Shadow (safe testing)
kubectl apply -f k8s/7-shadow-deployment.yaml

# All user traffic goes to Production
# Shadow gets mirrored traffic (read-only, no writes)

# Monitor shadow logs
kubectl logs -f deployment/aceest-shadow -n aceest-fitness

# When confident, promote shadow to production
kubectl patch deployment aceest-production -n aceest-fitness \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"aceest-fitness","image":"aceest-fitness:1.1.0"}]}}}}'

# Scale shadow down
kubectl scale deployment aceest-shadow --replicas=0 -n aceest-fitness
```

---

## 🔍 Monitoring Commands

### View All Resources
```bash
# Deployments
kubectl get deployments -n aceest-fitness

# Pods
kubectl get pods -n aceest-fitness -o wide

# Services
kubectl get services -n aceest-fitness

# Replica Sets
kubectl get rs -n aceest-fitness

# All resources
kubectl get all -n aceest-fitness
```

### Detailed Information
```bash
# Describe deployment
kubectl describe deployment aceest-blue -n aceest-fitness

# Describe pod
kubectl describe pod <pod-name> -n aceest-fitness

# Events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'

# Logs
kubectl logs <pod-name> -n aceest-fitness
kubectl logs -f <pod-name> -n aceest-fitness  # Follow logs

# Multiple pods
kubectl logs -f deployment/aceest-blue -n aceest-fitness
```

### Port Forward & Access
```bash
# Forward service to localhost
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Forward specific pod
kubectl port-forward -n aceest-fitness pod/<pod-name> 8080:5000

# Then access: http://localhost:8080
```

---

## 🔄 Rollback Procedures

### Automatic Rollback (via Readiness Probes)
If pods fail health checks, Kubernetes automatically:
- Restarts unhealthy pods (liveness probe)
- Removes from load balancer (readiness probe)

### Manual Rollback Commands

**Blue-Green:**
```bash
# Instant switch back to Blue
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"blue"}}}'
```

**Rolling Update:**
```bash
# Rollback to previous version
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness

# Rollback to specific revision
kubectl rollout undo deployment/aceest-rolling --to-revision=1 -n aceest-fitness

# View history
kubectl rollout history deployment/aceest-rolling -n aceest-fitness
```

**Canary:**
```bash
# Scale canary to 0
kubectl scale deployment aceest-canary --replicas=0 -n aceest-fitness
```

---

## 🛠️ Troubleshooting

### Pod Won't Start
```bash
# Check pod status
kubectl describe pod <pod-name> -n aceest-fitness

# Check logs
kubectl logs <pod-name> -n aceest-fitness

# Check events
kubectl get events -n aceest-fitness
```

### Service Not Accessible
```bash
# Check service
kubectl get service aceest-fitness-service -n aceest-fitness

# Check endpoints
kubectl get endpoints aceest-fitness-service -n aceest-fitness

# Check DNS
kubectl exec -it <pod-name> -n aceest-fitness -- nslookup aceest-fitness-service

# Port forward if issues
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80
```

### Deployment Stuck
```bash
# Check rollout status
kubectl rollout status deployment/aceest-blue -n aceest-fitness

# Check replica sets
kubectl get rs -n aceest-fitness

# Force delete pod (emergency)
kubectl delete pod <pod-name> -n aceest-fitness --grace-period=0 --force
```

---

## 📊 Performance Metrics

| Strategy | Rollback Time | Zero-Downtime | Risk |
|----------|---------------|---------------|------|
| Blue-Green | <1 second | ✅ Yes | Low |
| Canary | ~5 minutes | ✅ Yes | Very Low |
| Rolling | 5-10 minutes | ✅ (partial) | Medium |
| A/B Test | Gradual | ✅ Yes | Low |
| Shadow | <1 second | ✅ Yes | None |

---

## 📚 Additional Resources

- **Deployment Strategies Guide:** `k8s/DEPLOYMENT-STRATEGIES.md`
- **DevOps Report:** `DEVOPS-REPORT.md`
- **Quick Reference:** `QUICKREF.md`
- **Kubernetes Docs:** https://kubernetes.io/docs/

---

## 🎯 Typical Workflow

1. **Commit code to GitHub**
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. **Jenkins pipeline auto-triggers**
   - Builds Docker image
   - Runs tests
   - Checks code quality
   - Deploys to Kubernetes

3. **Monitor deployment**
   ```bash
   kubectl get pods -n aceest-fitness -w
   ```

4. **Test in environment**
   ```bash
   kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80
   ```

5. **Switch to production** (if Blue-Green)
   ```bash
   kubectl patch service aceest-fitness-service -n aceest-fitness \
     -p '{"spec":{"selector":{"variant":"green"}}}'
   ```

6. **Monitor metrics and logs**
   ```bash
   kubectl logs -f deployment/aceest-blue -n aceest-fitness
   ```

7. **Rollback if needed**
   ```bash
   kubectl rollout undo deployment/aceest-blue -n aceest-fitness
   ```

---

## 🚨 Emergency Operations

### Scale Down Service
```bash
kubectl scale deployment aceest-blue --replicas=0 -n aceest-fitness
```

### Delete All Pods (Force Restart)
```bash
kubectl delete pods --all -n aceest-fitness
```

### Check System Resources
```bash
kubectl top nodes
kubectl top pods -n aceest-fitness
```

### Enable Debug Mode
```bash
kubectl set env deployment/aceest-blue -n aceest-fitness DEBUG=true
```

---

**Remember:** Most of this happens automatically when you **run the Jenkins pipeline**! 🎉
