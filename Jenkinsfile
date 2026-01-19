
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out code..."
                checkout scm   // Auto‑checkout when using Multibranch
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
                sh "echo Build step goes here"
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                sh "echo Test step goes here"
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application..."
                sh "echo Deploy step goes here"
            }
        }
    }

    post {
        success {
            echo "✔ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
