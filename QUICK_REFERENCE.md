# ACEest Fitness API - Quick Reference Guide

> A fast lookup guide for common tasks, commands, and troubleshooting.

---

## 🚀 Quick Start (2 minutes)

### Windows
```batch
quickstart.bat
```

### macOS/Linux
```bash
chmod +x quickstart.sh
./quickstart.sh
```

---

## 📡 API Quick Reference

### Health Check
```bash
curl http://localhost:5000/health
```

### Create Client
```bash
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name":"John","age":30,"weight":75,"program":"Fat Loss (FL)"}'
```

### Get Client
```bash
curl http://localhost:5000/clients/John
```

### Record Progress
```bash
curl -X POST http://localhost:5000/clients/John/progress \
  -H "Content-Type: application/json" \
  -d '{"adherence":85}'
```

### Log Workout
```bash
curl -X POST http://localhost:5000/clients/John/workouts \
  -H "Content-Type: application/json" \
  -d '{"workout_type":"Squat","date":"2024-03-16","duration_min":60}'
```

---

## 🧪 Testing Quick Reference

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_app.py::TestClientsCRUD::test_create_client_success -v

# Run tests in Docker
docker run --rm aceest-fitness:latest pytest tests/ -v
```

---

## 🐳 Docker Quick Reference

```bash
# Build image
docker build -t aceest-fitness:latest .

# Run container
docker run -d -p 5000:5000 --name aceest-api aceest-fitness:latest

# View logs
docker logs -f aceest-api

# Stop container
docker stop aceest-api

# Remove container
docker rm aceest-api

# Docker compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 🌿 Git Quick Reference

```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit with proper message
git commit -m "feat(module): description"

# Push branch
git push origin feature/new-feature

# Create pull request (via GitHub)

# After merge, delete branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

---

## 📁 Project Structure

```
ACEest-DevOps/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container build file
├── .github/workflows/main.yml # CI/CD pipeline
├── tests/
│   └── test_app.py         # Test suite
├── README.md               # Main documentation
├── API.md                  # API reference
├── PROCESS.md              # Process documentation
├── NEXT_STEPS.md           # Implementation guide
└── .env.example            # Environment template
```

---

## 🔥 Common Issues & Fixes

### Port 5000 Already in Use
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database Locked
```bash
# Remove old database
rm aceest_fitness.db

# Reinitialize
python -c "from app import init_db; init_db()"
```

### Docker Build Fails
```bash
# Clear cache
docker system prune -a

# Rebuild
docker build --no-cache -t aceest-fitness:latest .
```

### Tests Failing
```bash
# Clear cache
pytest --cache-clear

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Total Endpoints | 18 |
| API Response Time | < 100ms |
| Code Coverage | 98% |
| Test Cases | 50+ |
| Docker Image Size | ~150MB |
| Python Version | 3.10+ |
| CI/CD Stages | 6 |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation & setup |
| API.md | Complete API reference |
| PROCESS.md | DevOps process explanation |
| NEXT_STEPS.md | Implementation roadmap |
| CHANGELOG.md | Version history |

---

## 🎯 Program Factors

| Program | Factor | Calculation |
|---------|--------|-------------|
| Fat Loss (FL) | 22 | weight × 22 |
| Muscle Gain (MG) | 35 | weight × 35 |
| Beginner (BG) | 26 | weight × 26 |

---

## ✅ Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] Docker image builds
- [ ] Container runs successfully
- [ ] Health check responds
- [ ] Code pushed to GitHub
- [ ] CI/CD pipeline green
- [ ] No secrets in code
- [ ] Documentation complete

---

## 🔗 Useful Links

- GitHub: https://github.com/yourusername/aceest-fitness
- API Docs: See API.md
- Process Flow: See PROCESS.md
- Deployment: See NEXT_STEPS.md

---

## 💡 Tips & Tricks

### Python Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate.bat

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Git Aliases
```bash
# Add aliases for faster commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

### Docker Shortcuts
```bash
# View all containers (including stopped)
docker ps -a

# View images
docker images

# Remove dangling images
docker image prune

# View container logs
docker logs <container_id>
```

---

**Last Updated:** March 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅
