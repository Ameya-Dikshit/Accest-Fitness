# ACEest Fitness DevOps Quick Reference

## What Was Implemented

✅ **CI/CD Pipeline (Jenkinsfile)**
- Automated build, test, and deploy
- Docker image creation
- Code quality checks
- Security scanning
- Graceful error handling

✅ **Kubernetes Deployment Strategies**
- Blue-Green (zero-downtime)
- Canary (gradual rollout)
- Rolling Update (standard deployment)
- A/B Testing (feature testing)
- Shadow (production testing)

✅ **Infrastructure as Code**
- 8 Kubernetes YAML manifests
- ConfigMap for configuration
- NetworkPolicy for security
- ResourceQuota for management
- PodDisruptionBudget for reliability

✅ **Testing & Quality**
- 34 Pytest unit tests
- Code linting (Flake8)
- Code formatting (Black)
- Vulnerability scanning (Trivy)

---

## Quick Commands

### View Resources
```bash
# Deployments
kubectl get deployments -n aceest-fitness

# Pods
kubectl get pods -n aceest-fitness

# Services
kubectl get services -n aceest-fitness

# All resources
kubectl get all -n aceest-fitness
```

### Deploy Strategies
```bash
# Blue-Green (zero-downtime)
kubectl apply -f k8s/3-blue-green-deployment.yaml
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"variant":"green"}}}'

# Canary (gradual)
kubectl apply -f k8s/4-canary-deployment.yaml

# Rolling (standard)
kubectl apply -f k8s/5-rolling-update-deployment.yaml

# A/B Test
kubectl apply -f k8s/6-ab-testing-deployment.yaml

# Shadow
kubectl apply -f k8s/7-shadow-deployment.yaml
```

### Rollback
```bash
# Rollback deployment
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness

# Rollback specific revision
kubectl rollout undo deployment/aceest-rolling --to-revision=2 -n aceest-fitness

# View history
kubectl rollout history deployment/aceest-rolling -n aceest-fitness
```

### Test Locally
```bash
# Port forward
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Test endpoint
curl http://localhost:8080/health

# View logs
kubectl logs -f deployment/aceest-rolling -n aceest-fitness

# Execute in pod
kubectl exec -it <pod-name> -n aceest-fitness -- /bin/sh
```

### Scale Deployment
```bash
# Scale to 5 replicas
kubectl scale deployment aceest-rolling --replicas=5 -n aceest-fitness

# Scale to 0 (delete)
kubectl scale deployment aceest-rolling --replicas=0 -n aceest-fitness
```

---

## File Locations

| What | Where |
|------|-------|
| Jenkins Pipeline | `Jenkinsfile` |
| Docker Build | `Dockerfile` |
| Unit Tests | `tests/test_app.py` |
| K8s Manifests | `k8s/` directory |
| Deployment Guide | `k8s/DEPLOYMENT-STRATEGIES.md` |
| DevOps Report | `DEVOPS-REPORT.md` |
| This Guide | `QUICKREF.md` |

---

## Git Repository

**URL:** https://github.com/Ameya-Dikshit/Accest-Fitness

**Latest Commits:**
```
59bdaf4 - Add comprehensive Kubernetes deployment manifests
673c4a6 - Make pipeline resilient: fallback when Docker/tools unavailable
2acd5a4 - Update pipeline for Docker-based testing
9958755 - Remove node labels from post section
69eb00c - Fix post section: wrap sh commands in node blocks
```

---

## Deployment Strategy Selection

| Need | Strategy | Time |
|------|----------|------|
| Zero downtime | Blue-Green | <1 sec |
| Safe gradual | Canary | 5-15 min |
| Standard | Rolling | 5-10 min |
| Feature test | A/B Test | Variable |
| Load test | Shadow | N/A (testing) |

---

## Health Monitoring

### Probes Configured
- **Liveness:** Restart unhealthy pods (every 10s)
- **Readiness:** Remove from load balancer (every 5s)
- **Health Endpoint:** `/health`

### Resource Limits
```yaml
requests:
  memory: "128Mi"
  cpu: "100m"
limits:
  memory: "512Mi"
  cpu: "500m"
```

### Auto-Scaling (Rolling Update)
- Min replicas: 3
- Max replicas: 10
- CPU target: 70%
- Memory target: 80%

---

## Troubleshooting

### Pod won't start
```bash
kubectl describe pod <name> -n aceest-fitness
kubectl logs <name> -n aceest-fitness
```

### Service not accessible
```bash
kubectl get endpoints aceest-fitness-service -n aceest-fitness
kubectl get svc -n aceest-fitness
```

### Deployment stuck
```bash
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'
kubectl rollout status deployment/aceest-rolling -n aceest-fitness
```

### Force delete pod
```bash
kubectl delete pod <name> -n aceest-fitness --grace-period=0 --force
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Docker Build Time | ~8 seconds |
| Image Size | 228MB |
| Test Suite Time | 5.22 seconds |
| Pods per Deployment | 3-5 replicas |
| Target Availability | 99.5% |

---

## Contact & Documentation

- **GitHub Repo:** https://github.com/Ameya-Dikshit/Accest-Fitness
- **Report:** See `DEVOPS-REPORT.md`
- **Deployment Guide:** See `k8s/DEPLOYMENT-STRATEGIES.md`
- **Dockerfile:** Multi-stage, production-optimized
- **Jenkinsfile:** Latest version with fallbacks
