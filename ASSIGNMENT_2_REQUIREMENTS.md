# Assignment 2 - DevOps CI/CD Implementation
## Complete Requirements & Deliverables Checklist

---

## ASSIGNMENT CONTEXT
- **Course:** Introduction to DEVOPS (CSIZG514/SEZG514) S1-25
- **Assignment Type:** DevOps CI/CD Implementation for ACEest Fitness & Gym
- **Role:** DevOps Engineer
- **Goal:** Establish robust, test-driven, fully automated DevOps pipeline with code quality, consistency, and reliability across multiple application versions

---

## KEY DIFFERENCES FROM ASSIGNMENT 1
Assignment 1 focused on: Jenkins CI/CD pipeline with Docker containerization
Assignment 2 adds: SonarQube, Docker Hub registry, Kubernetes deployment, advanced deployment strategies

---

## LEARNING OBJECTIVES (What They Want You to Achieve)

### 1. Apply DevOps Principles
- [ ] Design and implement fully automated complete CI/CD pipeline
- [ ] Show understanding of continuous integration and continuous delivery

### 2. Demonstrate Proficiency in Industry-Standard Tools
- [ ] **Version Control:** Git + GitHub (already done in Assignment 1)
- [ ] **Build Automation:** Jenkins (already done in Assignment 1)
- [ ] **Testing Framework:** Pytest (already done in Assignment 1)
- [ ] **Code Quality:** SonarQube (NEW - must add)
- [ ] **Containerization:** Docker (already done) or Podman (new option)
- [ ] **Container Registry:** Docker Hub / quay.io (NEW - must push images)
- [ ] **Deployment/Orchestration:** Minikube or Kubernetes on AWS/Azure/GCP (NEW - must implement)

### 3. Integrate Testing & Quality Validation
- [ ] Automated testing in CI pipeline
- [ ] Code quality gates enforced
- [ ] SonarQube integration in Jenkins

### 4. Progressive Deployment Strategies (NEW)
- [ ] Blue-Green Deployment
- [ ] Canary Release
- [ ] Shadow Deployment
- [ ] A/B Testing
- [ ] Rolling Update
- [ ] Rollback mechanisms for failure scenarios

### 5. Infrastructure Consistency
- [ ] Containerized deployment
- [ ] Kubernetes orchestration
- [ ] Infrastructure reliability

### 6. Collaborative Workflows
- [ ] Version control best practices
- [ ] Continuous improvement practices

---

## ASSIGNMENT TASKS & DELIVERABLES

### Task 1: Application Development
- [x] Flask web application (from Assignment 1)
- [x] Modular, maintainable code
- [x] Pythonic standards
- [ ] Ensure code is ready for SonarQube analysis

### Task 2: Version Control System Setup
- [x] Git repository initialized
- [x] GitHub repository linked
- [ ] Multiple versions tagged
- [ ] Commits tracked (features, bug fixes, infrastructure)
- [ ] Structured branching strategy

### Task 3: Unit Testing & Test Automation
- [x] Pytest tests implemented (from Assignment 1)
- [x] Automated test execution in CI pipeline
- [ ] Tests validated before build/deployment
- [ ] Code coverage reports

### Task 4: Continuous Integration with Jenkins (Enhanced)
- [x] Jenkins configured (from Assignment 1)
- [x] Git hooks for automatic builds
- [ ] **NEW:** Integrate SonarQube quality gates
- [ ] **NEW:** Push Docker images to registry
- [ ] Build artifacts for all versions
- [ ] Jenkins workflow shows successful recent runs

### Task 5: Containerization with Docker & Registry
- [x] Docker images created (from Assignment 1)
- [ ] **NEW:** Push images to Docker Hub / quay.io
- [ ] **NEW:** Version control Docker images (v1.0, v2.0, v3.0, etc.)
- [ ] **NEW:** All application versions in registry
- [ ] Image security scanning (optional but recommended)

### Task 6: Continuous Delivery & Deployment (NEW - MAJOR REQUIREMENT)
- [ ] **Kubernetes deployment (Minikube or Cloud)**
- [ ] **Blue-Green Deployment** - Maintain two identical environments
- [ ] **Canary Release** - Gradual rollout to subset of users
- [ ] **Shadow Deployment** - Test version without affecting users
- [ ] **A/B Testing** - Route traffic to different versions
- [ ] **Rolling Update** - Gradual instance replacement
- [ ] **Rollback mechanisms** - Revert to stable version on failure
- [ ] **Zero-downtime deployment**

### Task 7: Automated Build & Testing Integration (Enhanced)
- [ ] **NEW:** SonarQube integration
- [ ] **NEW:** Static code analysis in pipeline
- [ ] **NEW:** Quality gates enforcement
- [ ] **NEW:** Code quality reports
- [ ] Pytest execution in containerized environment
- [ ] Test result reporting in Jenkins
- [ ] Coverage reports

### Task 8: Advanced Pipeline Enhancements
- [ ] Multiple deployment stages in pipeline
- [ ] Pre-deployment quality checks
- [ ] Automated rollback triggers
- [ ] Deployment strategy selection
- [ ] Health checks post-deployment

---

## SUBMISSION REQUIREMENTS

### Code & Configuration Files
- [ ] Flask application files
- [ ] Jenkinsfile (enhanced with SonarQube and Kubernetes steps)
- [ ] Dockerfile (already have)
- [ ] **NEW:** Kubernetes YAML manifests for:
  - [ ] Deployment
  - [ ] Service
  - [ ] ConfigMap
  - [ ] PersistentVolume (if needed)
- [ ] **NEW:** SonarQube configuration
- [ ] Pytest test cases
- [ ] requirements.txt

### GitHub Repository
- [ ] Public repository (or with invited access)
- [ ] All code committed and pushed
- [ ] Multiple versions tagged
- [ ] README with setup instructions
- [ ] Link provided for review

### Docker Hub / Registry
- [ ] **NEW:** Public Docker Hub account / registry
- [ ] **NEW:** All application versions pushed:
  - [ ] aceest-fitness:1.0
  - [ ] aceest-fitness:2.0
  - [ ] aceest-fitness:3.0
  - [ ] aceest-fitness:latest
- [ ] Registry link provided

### Kubernetes Cluster
- [ ] **NEW:** Minikube running locally OR
  - [ ] AWS EKS cluster
  - [ ] Azure AKS cluster
  - [ ] GCP GKE cluster
- [ ] **NEW:** Cluster endpoint URL provided
- [ ] **NEW:** All deployment strategies running:
  - [ ] Blue-Green setup visible
  - [ ] Canary deployment working
  - [ ] Rolling update demonstrated
  - [ ] Rollback mechanism tested
- [ ] Cluster accessible for review

### SonarQube Instance
- [ ] **NEW:** SonarQube installed (local or cloud)
- [ ] **NEW:** Quality gates configured
- [ ] **NEW:** Analysis results available
- [ ] **NEW:** Code quality report generated
- [ ] Metrics dashboard accessible

### Jenkins Demonstration
- [ ] Jenkins running and accessible
- [ ] aceest-fitness-pipeline job configured
- [ ] Recent successful builds shown
- [ ] Build history visible
- [ ] Pipeline stages executing:
  1. Checkout
  2. Build
  3. Unit Tests
  4. SonarQube Analysis (NEW)
  5. Code Quality Gate Check (NEW)
  6. Docker Build
  7. Push to Registry (NEW)
  8. Deploy to Kubernetes (NEW)
  9. Blue-Green Deployment (NEW)
  10. Smoke Tests
  11. Canary Deployment (NEW)
  12. Rollback Check (NEW)

### Report (2-3 Pages)
- [ ] **NEW:** CI/CD architecture overview with diagram
- [ ] **NEW:** Kubernetes deployment strategy explanation
- [ ] **NEW:** SonarQube integration details
- [ ] **NEW:** Docker Hub integration details
- [ ] Challenges faced and mitigation strategies
- [ ] Advanced deployment strategies implemented
- [ ] Key automation outcomes
- [ ] Testing and quality metrics
- [ ] Performance improvements

---

## CRITICAL NEW REQUIREMENTS FOR ASSIGNMENT 2

### 1. SonarQube Code Quality
```
Priority: HIGH
Tasks:
- Install SonarQube (local Docker or cloud)
- Integrate with Jenkins pipeline
- Configure quality gates (e.g., minimum 80% coverage)
- Generate and publish code quality reports
- Show SonarQube dashboard in submission
```

### 2. Docker Hub Registry Push
```
Priority: HIGH
Tasks:
- Create Docker Hub account
- Configure Docker credentials in Jenkins
- Push images with proper versioning
- Tag images: v1.0, v2.0, v3.0, latest
- Keep registry public/accessible for review
```

### 3. Kubernetes Deployment
```
Priority: CRITICAL
Tasks:
- Install Minikube locally OR
- Deploy to AWS/Azure/GCP
- Create deployments for each version
- Create services for load balancing
- Create namespaces if needed
- Configure persistent storage if needed
- Provide endpoint URL for access
```

### 4. Advanced Deployment Strategies
```
Priority: CRITICAL (Each must be demonstrated)

A. Blue-Green Deployment:
   - Maintain v1 (Blue) and v2 (Green) simultaneously
   - Switch traffic between versions instantly
   - Zero downtime

B. Canary Release:
   - Route 10% traffic to new version
   - 90% to stable version
   - Gradually increase percentage
   - Rollback if errors detected

C. Shadow Deployment:
   - Route subset of traffic to new version
   - Users don't know they're being tested
   - Monitor metrics separately

D. A/B Testing:
   - Split users into groups
   - Route Group A to version 1
   - Route Group B to version 2
   - Compare metrics and behavior

E. Rolling Update:
   - Replace pods one by one
   - Maintain service availability
   - No downtime

F. Rollback Mechanism:
   - Trigger: Quality gate failure, health check failure
   - Revert to previous stable version
   - Automatic or manual rollback
```

### 5. Kubernetes YAML Manifests
```
Required files:
- deployment.yaml (v1, v2, v3)
- service.yaml (LoadBalancer/ClusterIP)
- namespace.yaml (if using namespaces)
- ingress.yaml (if using ingress)
- configmap.yaml (configuration)
- hpa.yaml (Horizontal Pod Autoscaler - optional)
```

### 6. Jenkins Pipeline Enhancements
```
New stages to add:
1. SonarQube Analysis
   - Run: sonar-scanner
   - Publish results
   - Check quality gates

2. Push to Registry
   - Docker login to Hub
   - Push image with version tags
   - Update latest tag

3. Deploy to Kubernetes
   - Apply deployment manifests
   - Wait for rollout

4. Blue-Green Switch
   - Switch service endpoint
   - Health checks

5. Canary Deployment
   - Scale new version 10%
   - Monitor metrics

6. Rollback Check
   - Verify deployment health
   - Rollback if threshold exceeded
```

---

## DEPLOYMENT STRATEGIES IMPLEMENTATION GUIDE

### Blue-Green Deployment
```yaml
- Two deployments: acme-fitness-blue (v1), acme-fitness-green (v2)
- Service initially points to blue
- Deploy green alongside blue
- Switch service selector to green after validation
- Keep blue running for instant rollback
```

### Canary Release
```yaml
- Main deployment runs v1 (90%)
- Canary deployment runs v2 (10%)
- Route via Istio or native K8s weight distribution
- Monitor metrics
- Gradually increase % to v2
- Rollback if metrics degrade
```

### Rolling Update
```yaml
- Set maxSurge: 25% and maxUnavailable: 25% in deployment
- K8s automatically creates new pods with v2
- Terminates old pods with v1
- Continues until all pods updated
- Maintains service availability
```

### A/B Testing
```yaml
- Label pods: version=v1, version=v2
- Route traffic based on labels
- Track conversion metrics per version
- Route more traffic to winning version
```

---

## TESTING CHECKLIST FOR EACH DEPLOYMENT STRATEGY

For each strategy, you must demonstrate:
- [ ] Initial state (version X running)
- [ ] Deployment process (version Y being deployed)
- [ ] Validation (version Y receives traffic)
- [ ] Rollback scenario (trigger failure and revert)
- [ ] Success criteria (service always available)
- [ ] Metrics collected (response time, error rate, user count)

---

## SUBMISSION CHECKLIST

### Before Submission
- [ ] GitHub repo is public/accessible
- [ ] All code committed and pushed
- [ ] Docker images pushed to registry
- [ ] Kubernetes cluster running with all 5 versions
- [ ] All 6 deployment strategies demonstrated
- [ ] Jenkins shows recent successful builds
- [ ] SonarQube reports generated
- [ ] Endpoint URLs verified working
- [ ] Report written (2-3 pages)

### Final Submission Items
1. [ ] GitHub repository link
2. [ ] Docker Hub repository link
3. [ ] Kubernetes cluster endpoint URL
4. [ ] SonarQube dashboard URL (if accessible)
5. [ ] Jenkins dashboard URL
6. [ ] 2-3 page report (PDF or DOCX)
7. [ ] Screenshots of:
   - [ ] All deployments running
   - [ ] Blue-Green switch
   - [ ] Canary deployment
   - [ ] Rolling update
   - [ ] Rollback execution
   - [ ] SonarQube results
   - [ ] Jenkins pipeline execution

---

## TIMELINE RECOMMENDATION

### Week 1: SonarQube & Code Quality
- Integrate SonarQube
- Run analysis
- Fix code issues
- Achieve quality gates

### Week 2: Docker Hub Registry
- Push images
- Version management
- Verify registry

### Week 3: Kubernetes Setup
- Install Minikube / Cloud
- Create YAML manifests
- Deploy basic version

### Week 4: Deployment Strategies
- Implement Blue-Green
- Implement Canary
- Implement Rolling Update

### Week 5: Advanced Strategies
- Shadow Deployment
- A/B Testing
- Rollback mechanisms

### Week 6: Testing & Documentation
- Test all scenarios
- Document deployment steps
- Write report
- Create demonstration

---

## SUCCESS METRICS

Assignment will be evaluated on:
1. **CI/CD Pipeline Automation:** 25%
   - All stages executing automatically
   - Build success rate
   - Deployment consistency

2. **Code Quality & Testing:** 20%
   - SonarQube scores
   - Test coverage
   - Quality gate status

3. **Containerization & Registry:** 15%
   - Docker images in registry
   - Version management
   - Image sizes optimized

4. **Kubernetes Deployment:** 20%
   - Cluster running
   - Manifests well-structured
   - Services accessible

5. **Deployment Strategies:** 15%
   - All 6 strategies demonstrated
   - Zero-downtime confirmed
   - Rollback successful
   - Monitoring/metrics in place

6. **Documentation & Report:** 5%
   - Clear architecture diagram
   - Step-by-step instructions
   - Challenge resolution explained

---

## RESOURCES & REFERENCES

### Tools to Install/Use
1. **SonarQube:** docker run -d -p 9000:9000 sonarqube
2. **Minikube:** minikube start --cpus=4 --memory=8192
3. **kubectl:** For cluster management
4. **Docker Hub:** Create free account
5. **Jenkins:** Already have from Assignment 1

### Kubernetes Deployment Commands
```bash
# Create namespace
kubectl create namespace acme-fitness

# Apply deployment
kubectl apply -f deployment.yaml -n acme-fitness

# Check status
kubectl get deployments -n acme-fitness
kubectl get pods -n acme-fitness
kubectl get svc -n acme-fitness

# Port forward for access
kubectl port-forward svc/acme-fitness 5000:5000 -n acme-fitness

# Rollout commands
kubectl rollout status deployment/acme-fitness -n acme-fitness
kubectl rollout history deployment/acme-fitness -n acme-fitness
kubectl rollout undo deployment/acme-fitness -n acme-fitness
```

---

## NEXT STEPS FROM ASSIGNMENT 1

You already have:
✅ Flask REST API with 18 endpoints
✅ Pytest test suite (34 tests)
✅ Docker containerization
✅ Jenkins CI/CD pipeline
✅ GitHub repository
✅ Git version control

Now you need to add:
❌ SonarQube integration & quality gates
❌ Docker Hub repository with versioned images
❌ Kubernetes cluster (Minikube or Cloud)
❌ Kubernetes YAML manifests (deployment, service, etc.)
❌ Advanced deployment strategies (6 types)
❌ Rollback mechanisms
❌ Endpoint URL of running cluster
❌ Updated Jenkins pipeline with new stages
❌ 2-3 page report

