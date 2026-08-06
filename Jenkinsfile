pipeline {
    agent any

    environment {
        IMAGE_NAME = "tanayyyy/flask-two-tier-app"
        EC2_HOST   = "54.242.134.32"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker compose build
                '''
            }
        }

        stage('Run Containers') {
            steps {
                sh '''
                docker compose down --remove-orphans || true
                docker rm -f mysql flask-app 2>/dev/null || true
                docker compose up --build -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                echo "Waiting for application..."
                sleep 15

                docker exec flask-app python -c "
import urllib.request
print(urllib.request.urlopen('http://localhost:5000/health').read().decode())
"
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker tag flask-two-tier-ci-flask-app:latest $IMAGE_NAME:latest
                    docker tag flask-two-tier-ci-flask-app:latest $IMAGE_NAME:$BUILD_NUMBER

                    docker push $IMAGE_NAME:latest
                    docker push $IMAGE_NAME:$BUILD_NUMBER

                    docker logout
                    '''
                }
            }
        }

        stage('Test SSH Connection') {
            steps {
                sshagent(credentials: ['EC2 SSH']) {

                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@$EC2_HOST "echo 'SSH Connection Successful' && hostname && pwd"
                    '''

                }
            }
        }

    }

    post {

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }

    }
}