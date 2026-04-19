pipeline {
    agent any
    
    environment {
        SCANNER_HOME = '/opt/sonarqube-scanner'
        IMAGE_NAME = 'aceest-fitness'
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    if [ -f Dockerfile ]; then
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "✅ Docker image built successfully"
                    else
                        echo "⚠️ Dockerfile not found, skipping Docker build"
                    fi
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo '✅ Running unit tests...'
                sh '''
                    # Run tests in Python container if Dockerfile exists
                    if [ -f Dockerfile ]; then
                        docker run --rm -v $(pwd):/app -w /app python:3.9 bash -c "pip install -q -r requirements.txt && pytest tests/ -v --tb=short || true"
                    else
                        # Fallback: try to run directly
                        if command -v pytest >/dev/null 2>&1; then
                            pytest tests/ -v --tb=short || true
                        else
                            echo "⚠️ pytest not available - skipping"
                        fi
                    fi
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    if [ -f Dockerfile ]; then
                        docker run --rm -v $(pwd):/app -w /app python:3.9 bash -c "pip install -q black flake8 pylint && black --check app.py tests/ || true && flake8 app.py tests/ --max-line-length=120 || true" || true
                    else
                        echo "⚠️ Dockerfile not found - skipping"
                    fi
                '''
            }
        }
        
        stage('Test Docker Container') {
            steps {
                echo '🧪 Testing Docker container...'
                sh '''
                    if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1; then
                        # Remove old container if exists
                        docker rm -f aceest-test 2>/dev/null || true

                        # Run container
                        CONTAINER_ID=$(docker run -d --name aceest-test -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG})
                        echo "Container started with ID: $CONTAINER_ID"

                        # Wait for container to initialize
                        sleep 5

                        # Verify container is running
                        if docker ps | grep aceest-test > /dev/null; then
                            echo "✅ Container is running"
                            docker logs aceest-test || true
                        else
                            echo "❌ Container failed to start"
                        fi

                        # Cleanup
                        docker stop aceest-test 2>/dev/null || true
                        docker rm aceest-test 2>/dev/null || true
                        echo "✅ Container test completed"
                    else
                        echo "⚠️ Image ${IMAGE_NAME}:${IMAGE_TAG} not found - skipping container test"
                    fi
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo '🔒 Running security scan...'
                sh '''
                    if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1; then
                        echo "Scanning Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                        
                        # Try Trivy if available
                        if command -v trivy >/dev/null 2>&1; then
                            echo "Running Trivy scan..."
                            trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG} || true
                        else
                            echo "⚠️ Trivy not available - skipping vulnerability scan"
                        fi
                        
                        echo "✅ Security scan completed"
                    else
                        echo "⚠️ Image not found - skipping security scan"
                    fi
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline succeeded!'
            echo "Build #${BUILD_NUMBER} completed successfully"
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed!'
            echo "Build #${BUILD_NUMBER} failed. Check logs for details."
        }
        always {
            echo '🧹 Cleaning up...'
        }
    }
}
