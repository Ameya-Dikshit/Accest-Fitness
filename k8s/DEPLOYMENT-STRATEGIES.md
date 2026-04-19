# ACEest Fitness - Kubernetes Deployment Strategies Guide

## Overview
This directory contains comprehensive Kubernetes manifests implementing industry-standard deployment strategies for the ACEest Fitness application.

## File Structure

| File | Purpose | Strategy |
|------|---------|----------|
| `0-namespace.yaml` | Kubernetes namespace for app isolation | Foundation |
| `1-configmap.yaml` | Application configuration | Configuration |
| `2-service.yaml` | Network service exposure | Networking |
| `3-blue-green-deployment.yaml` | Blue-Green deployment strategy | Zero-downtime switching |
| `4-canary-deployment.yaml` | Canary release strategy | Gradual rollout |
| `5-rolling-update-deployment.yaml` | Rolling update + HPA | Automatic scaling |
| `6-ab-testing-deployment.yaml` | A/B testing variants | User segmentation |
| `7-shadow-deployment.yaml` | Shadow deployment | Safe testing |
| `8-rollback-recovery.yaml` | PDB, NetworkPolicy, Quotas | Resilience |

---

## Deployment Strategies Explained

### 1. **Blue-Green Deployment** (3-blue-green-deployment.yaml)
**When to use:** For zero-downtime deployments with complete version switches

**How it works:**
- Two identical deployments: Blue (current) and Green (new)
- Service switches selector from blue to green
- If issues detected, switch back to blue

**Rollback mechanism:**
```bash
# Switch back to blue (current production)
kubectl patch service aceest-fitness-service -p '{"spec":{"selector":{"variant":"blue"}}}'
```

**Advantages:**
- Complete rollback in seconds
- Full testing of new version before switch
- Zero data loss

---

### 2. **Canary Deployment** (4-canary-deployment.yaml)
**When to use:** For gradual, safe rollouts to monitor metrics

**How it works:**
- 1 pod of new version (canary) alongside 3 stable pods
- Route 5-10% traffic to canary
- Monitor error rates and metrics
- Gradually increase traffic if healthy

**Progression:**
```
10% (Canary 1) → 25% (Canary 2) → 50% (Canary 3) → 100% (All new)
```

**Rollback mechanism:**
```bash
# Reduce canary replicas to 0
kubectl scale deployment aceest-canary --replicas=0 -n aceest-fitness
```

---

### 3. **Rolling Update** (5-rolling-update-deployment.yaml)
**When to use:** Standard continuous deployment with no manual switching

**How it works:**
- Replaces pods one-by-one (maxUnavailable: 1)
- Allows up to 2 extra pods during update (maxSurge: 2)
- Automatic rollback on readiness probe failure

**Configuration:**
```yaml
maxSurge: 2        # 2 extra pods during update
maxUnavailable: 1  # Allow 1 unavailable
```

**Rollback mechanism:**
```bash
# Kubernetes auto-detects failures via readiness probes
# Manual rollback:
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness
```

**With HPA Scaling:**
- Automatically scales from 3-10 replicas based on CPU/Memory
- Safe during rolling updates

---

### 4. **A/B Testing** (6-ab-testing-deployment.yaml)
**When to use:** Testing new features with specific user segments

**How it works:**
- Two deployments: Variant A (current) and Variant B (new)
- Service routes to BOTH variants
- Client identifier determines which variant they see
- Metrics compare performance

**Traffic routing:**
```
Variant A: 50% of traffic (v1.0.0)
Variant B: 50% of traffic (v1.1.0)
```

**Rollback mechanism:**
```bash
# Scale down variant B
kubectl scale deployment aceest-variant-b --replicas=0 -n aceest-fitness
```

---

### 5. **Shadow Deployment** (7-shadow-deployment.yaml)
**When to use:** Testing new version in production without affecting users

**How it works:**
- Production deployment serves all real traffic
- Shadow deployment mirrors ALL requests (read-only)
- New version processes same data without writing
- Safe testing of performance impact

**Key features:**
```yaml
SHADOW_MODE: "true"
WRITE_OPERATIONS: "disabled"
```

**Rollback mechanism:**
- Instant: just scale shadow replicas to 0
- No production impact

---

## Deployment Workflow

### Deploy Blue-Green (zero-downtime):
```bash
# Deploy namespace
kubectl apply -f 0-namespace.yaml

# Deploy config and service
kubectl apply -f 1-configmap.yaml 2-service.yaml

# Deploy blue-green
kubectl apply -f 3-blue-green-deployment.yaml

# Test blue deployment
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# When ready, scale green and test
kubectl scale deployment aceest-green --replicas=3 -n aceest-fitness

# Switch traffic to green
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"variant":"green"}}}'

# If issues, rollback to blue
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"variant":"blue"}}}'
```

### Deploy Canary (gradual):
```bash
# Deploy stable + canary
kubectl apply -f 4-canary-deployment.yaml

# Monitor metrics for 10 minutes
watch 'kubectl get pods -n aceest-fitness'

# If healthy, increase canary replicas gradually
kubectl scale deployment aceest-canary --replicas=2 -n aceest-fitness
kubectl scale deployment aceest-canary --replicas=3 -n aceest-fitness

# Eventually scale stable down and canary up
kubectl scale deployment aceest-stable --replicas=0 -n aceest-fitness
```

### Deploy with Rolling Update:
```bash
# Just apply - Kubernetes handles the rolling update
kubectl apply -f 5-rolling-update-deployment.yaml

# Monitor rollout
kubectl rollout status deployment/aceest-rolling -n aceest-fitness

# If issues, automatic rollback via readiness probes
# Manual rollback:
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness
```

### Deploy A/B Testing:
```bash
# Deploy both variants
kubectl apply -f 6-ab-testing-deployment.yaml

# Route application should use 'variant' header or cookie
# Example: variant=a or variant=b

# Monitor metrics per variant
kubectl logs -l variant=a -n aceest-fitness
kubectl logs -l variant=b -n aceest-fitness

# Promote winning variant
# Scale down losing variant
kubectl scale deployment aceest-variant-a --replicas=0 -n aceest-fitness
```

### Deploy Shadow:
```bash
# Deploy production + shadow
kubectl apply -f 7-shadow-deployment.yaml

# New version runs in parallel
# Monitor shadow logs without affecting users

# When confident, promote shadow to production
kubectl patch deployment aceest-production -p '{"spec":{"template":{"spec":{"containers":[{"name":"aceest-fitness","image":"aceest-fitness:new-version"}]}}}}'

# Scale shadow down
kubectl scale deployment aceest-shadow --replicas=0 -n aceest-fitness
```

---

## Rollback Procedures

### Automatic Rollback (triggered by readiness probe):
- If pod health checks fail, Kubernetes automatically rollsback
- Requires proper `readinessProbe` configuration

### Manual Rollback:
```bash
# List deployment history
kubectl rollout history deployment/aceest-rolling -n aceest-fitness

# Rollback to previous version
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness

# Rollback to specific revision
kubectl rollout undo deployment/aceest-rolling --to-revision=2 -n aceest-fitness
```

### Emergency Rollback (Blue-Green):
```bash
# Instant switch back to blue
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"variant":"blue"}}}'
```

---

## Monitoring & Health Checks

### Liveness Probe (restart unhealthy pods):
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

### Readiness Probe (remove from load balancer):
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 2
```

### PodDisruptionBudget (maintain availability):
- Ensures minimum 2 pods always available
- Prevents kubectl drain from breaking service

---

## Performance Characteristics

| Strategy | Downtime | Risk | Speed | Testing |
|----------|----------|------|-------|---------|
| Blue-Green | 0 | Low | Medium | Full |
| Canary | 0 | Very Low | Slow | Incremental |
| Rolling | Minimal | Medium | Medium | Automatic |
| A/B Test | 0 | Low | Medium | User-based |
| Shadow | 0 | Very Low | Medium | Read-only |

---

## Best Practices

1. **Always use readiness probes** - Prevents broken deployments
2. **Set resource limits** - Prevents node resource exhaustion
3. **Use PodDisruptionBudget** - Maintains availability
4. **Monitor deployment** - Watch logs and metrics
5. **Test rollback** - Verify rollback works before production
6. **Use network policies** - Segment traffic safely
7. **Set resource quotas** - Prevent namespace resource hogging

---

## Kubernetes Commands Reference

```bash
# View deployments
kubectl get deployments -n aceest-fitness

# View pods
kubectl get pods -n aceest-fitness -o wide

# View services
kubectl get services -n aceest-fitness

# View logs
kubectl logs -f deployment/aceest-rolling -n aceest-fitness

# Port forward to test locally
kubectl port-forward -n aceest-fitness svc/aceest-fitness-service 8080:80

# Describe deployment
kubectl describe deployment aceest-rolling -n aceest-fitness

# Execute command in pod
kubectl exec -it <pod-name> -n aceest-fitness -- /bin/sh

# Get deployment history
kubectl rollout history deployment/aceest-rolling -n aceest-fitness

# View current replica status
kubectl get rs -n aceest-fitness
```

---

## Troubleshooting

### Pods not starting:
```bash
kubectl describe pod <pod-name> -n aceest-fitness
kubectl logs <pod-name> -n aceest-fitness
```

### Service not accessible:
```bash
kubectl get svc -n aceest-fitness
kubectl get endpoints -n aceest-fitness
```

### Deployment stuck:
```bash
# Check events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'

# Force rollback
kubectl rollout undo deployment/aceest-rolling -n aceest-fitness
```

---

## Deployment Selection Guide

**Use Blue-Green when:** Need guaranteed zero downtime with instant rollback

**Use Canary when:** Want to minimize risk by testing with real traffic gradually

**Use Rolling when:** Standard deployment with automatic health checks

**Use A/B when:** Testing new features with user segmentation

**Use Shadow when:** Testing without any production impact

