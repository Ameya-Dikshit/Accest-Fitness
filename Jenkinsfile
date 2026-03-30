pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    environment {
        IMAGE_NAME = 'aceest-fitness'
        IMAGE_TAG = "${BUILD_NUMBER}"
        REGISTRY = 'docker'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out code...'
                checkout scm
                sh 'git log -1 --oneline'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '📦 Setting up Python environment...'
                sh '''
                    python --version
                    python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint & Code Quality') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    black --check app.py tests/ || true
                    flake8 app.py tests/ --max-line-length=120 || true
                    pylint app.py --disable=all --enable=E || true
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo '✅ Running unit tests...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    pytest tests/ -v --cov=app --cov-report=xml --cov-report=html --tb=short
                '''
            }
            post {
                always {
                    // Archive coverage report
                    publishHTML([
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: true
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }
        
        stage('Test Docker Container') {
            steps {
                echo '🧪 Testing Docker container...'
                sh '''
                    # Remove old container if exists
                    docker rm -f aceest-test || true
                    
                    # Run container
                    docker run -d --name aceest-test -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    
                    # Wait for startup
                    sleep 2
                    
                    # Test health endpoint
                    curl -f http://localhost:5001/health || exit 1
                    
                    # Clean up
                    docker stop aceest-test
                    docker rm aceest-test
                    
                    echo "✅ Docker container health check passed"
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo '🔒 Running security scan with Trivy...'
                sh '''
                    # Install Trivy if needed
                    command -v trivy >/dev/null 2>&1 || {
                        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                    }
                    
                    # Scan image
                    trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG} || true
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo '📦 Archiving build artifacts...'
                sh '''
                    # Save Docker image details
                    docker inspect ${IMAGE_NAME}:${IMAGE_TAG} > docker-image-details.json || true
                    
                    # Save test results
                    ls -la htmlcov/ || true
                '''
                archiveArtifacts artifacts: 'docker-image-details.json,htmlcov/**', 
                                   allowEmptyArchive: true
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline succeeded!'
            sh '''
                echo "Build #${BUILD_NUMBER} completed successfully"
                echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
            '''
        }
        failure {
            echo '❌ Pipeline failed!'
            sh 'echo "Build #${BUILD_NUMBER} failed. Check logs for details."'
        }
        always {
            echo '🧹 Cleaning up...'
            sh '''
                # Clean up Docker resources
                docker system prune -f || true
            '''
            
            // Always delete workspace after build
            deleteDir()
        }
    }
}
