pipeline {
    agent any

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
                sh 'curl http://localhost:5000/health'
            }
        }
    }

    post {
        success {
            echo 'Application deployed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}