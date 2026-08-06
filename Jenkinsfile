pipeline {
    agent any

    environment {
        IMAGE_NAME = "tanayyyy/flask-two-tier-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Repository checked out by Jenkins'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 15
                docker exec flask-app python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read().decode())"
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
                sshagent(credentials: ['ec2-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@54.242.134.32 "echo SSH Connection Successful"
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