# ACEest Fitness - DevOps CI/CD Pipeline

This is a fitness management system built with Flask REST API. The project demonstrates a complete DevOps transformation journey from a simple application to a fully automated, containerized, and orchestrated system with continuous integration and deployment.

## Assignment 1: Application Development
We developed a Flask REST API for fitness management with 18 endpoints covering client management, workout tracking, progress monitoring, and metrics recording. The system uses SQLite3 database and includes 34 comprehensive test cases achieving 50% code coverage. The application was built following industry best practices with proper version control and modular code structure.

## Assignment 2: DevOps Transformation
We transformed the application into a system by containerizing it with Docker, setting up an automated 13-stage CI/CD pipeline using Jenkins, deploying to Kubernetes with 5 different deployment strategies, integrating SonarQube for continuous code quality analysis, and pushing Docker images to GitHub Container Registry. We implemented zero-downtime deployments and verified all deployment strategies work seamlessly.

## Knowledge Gained
We learned how to build scalable infrastructure as code, automate testing and deployment pipelines, implement multiple deployment strategies for different use cases, and monitor code quality throughout the development cycle. The key insight was understanding how DevOps bridges development and operations by automating everything from code commit to production deployment, reducing manual errors and enabling rapid iterations.

## Key Achievements
- Pylint score of 10.00/10 with Black-formatted code
- 5 deployment strategies successfully deployed and tested
- Zero-downtime deployment verified with Blue-Green switching
- Fully automated 13-stage pipeline from code commit to production
- 4 Docker images pushed to registry with proper versioning
- Complete security scanning and code quality gates

## Tools & Technologies

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | Flask |
| Database | SQLite3 |
| Containerization | Docker |
| Orchestration | Kubernetes |
| CI/CD | Jenkins |
| Code Quality | SonarQube |
| Registry | GitHub Container Registry |
| Security | Trivy |
| Version Control | Git/GitHub |

## What We Migrated

- **Local development** → **Containerized** (Docker)
- **Manual testing** → **Automated testing** (Pytest, 34 tests)
- **Manual deployment** → **CI/CD pipeline** (Jenkins)
- **Single deployment** → **Multiple strategies** (Blue-Green, Canary, A/B, Shadow)
- **Manual monitoring** → **Automated health checks** (Kubernetes)


## Quick Links

- **Repository:** https://github.com/Ameya-Dikshit/Accest-Fitness
- **Docker Images:** `ghcr.io/ameya-dikshit/aceest-fitness` (v1.0, v2.0, v3.0, latest)
- **Jenkins Pipeline:** `http://localhost:8080/job/aceest-fitness-pipeline/`
- **Kubernetes Endpoint:** `http://192.168.49.2:30258` (Blue-Green Service)

## Project Structure

```
aceest-fitness/
├── app.py                      # Flask REST API
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container image
├── Jenkinsfile                 # 13-stage CI/CD pipeline
├── k8s/                        # Kubernetes manifests
│   ├── 0-namespace.yaml
│   ├── 1-configmap.yaml
│   ├── 2-service.yaml
│   ├── 3-blue-green-deployment.yaml
│   ├── 4-canary-deployment.yaml
│   ├── 5-rolling-update-deployment.yaml
│   ├── 6-ab-testing-deployment.yaml
│   ├── 7-shadow-deployment.yaml
│   └── 8-rollback-recovery.yaml
├── tests/
│   ├── test_app.py             # 34 test cases
│   └── __init__.py
└── README.md
```
