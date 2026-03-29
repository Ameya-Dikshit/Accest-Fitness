# 🐳 How to Start Docker & Jenkins

## ⚠️ Docker Issue Detection

Your system shows: **Docker daemon is not running**

---

## ✅ Solution 1: Start Docker Desktop (Windows)

### Option A: Using GUI (Easiest)
1. **Open Start Menu**
2. **Search:** "Docker"
3. **Click:** "Docker Desktop" to launch
4. **Wait:** Until Docker icon appears in system tray (bottom right)
5. **Verify:** Icon should show whale logo ✓

### Option B: Using PowerShell
```powershell
# Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker.exe"

# Wait for it to start (30-60 seconds)
Start-Sleep 30

# Verify Docker is running
docker ps

# Should show: No errors, blank container list
```

### Option C: Using WSL2 Backend (If you have it)
```powershell
# Check if WSL2 is installed
wsl --list -v

# If not, Docker Desktop settings usually handle this automatically
```

---

## 🔍 Troubleshooting

### If Docker Still Won't Start:

**Check if Docker is installed:**
```powershell
docker --version

# Should show: Docker version 20.10.x or newer
```

**If Not Installed:**
1. Download from: https://www.docker.com/products/docker-desktop
2. Install Docker Desktop for Windows
3. Restart your computer
4. Try again

**If Port 8080 or 50000 is in use:**
```powershell
# Find what's using port 8080
netstat -ano | findstr :8080

# If something is using it, kill it:
taskkill /PID <PID> /F

# Use different ports instead:
docker run -d -p 8081:8080 -p 50001:50000 ...
```

---

## ✅ Solution 2: Run Jenkins Without Docker

### Option: Use Jenkins WAR file directly

```bash
# Download Jenkins
curl -o jenkins.war http://mirrors.jenkins.io/war-stable/latest/jenkins.war

# Run Jenkins directly
java -jar jenkins.war --port=8080

# Access: http://localhost:8080
```

---

## ✅ Solution 3: Simple Jenkins Alternative (Lightweight)

Instead of full Jenkins (which is heavy), use **GitHub Actions** (already configured!):

1. Push code to GitHub
2. Actions tab auto-runs pipeline
3. No setup needed!

---

## Once Docker is Running:

```powershell
# Run Jenkins
docker run -d -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  --name jenkins `
  jenkins/jenkins:latest

# Get initial password (wait 30 seconds first)
Start-Sleep 30
docker logs jenkins | findstr "initialAdminPassword"

# Open browser
Start-Process "http://localhost:8080"
```

---

## 📋 Quick Checklist

- [ ] Docker Desktop installed (`C:\Program Files\Docker\Docker\Docker.exe`)
- [ ] Docker Desktop running (whale icon in taskbar)
- [ ] Ports 8080 & 50000 available
- [ ] No firewall blocking Docker sockets

---

**Next Steps:**
1. Start Docker Desktop
2. Wait 2 minutes for it to initialize
3. Run the Jenkins command
4. Access http://localhost:8080

---

**Questions?** See [JENKINS_SETUP.md](JENKINS_SETUP.md) for detailed guide
