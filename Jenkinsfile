pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker build -t kisaafatimadocker/weather-app1 .'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests
                    sh 'pytest tests/'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub
                    sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
                    // Push Docker image
                    sh 'docker push kisaafatimadocker/weather-app1'
                }
            }
        }
    }
}