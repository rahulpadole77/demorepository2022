
pipeline {
    agent any   // Use any available Jenkins agent/runner

    environment {
        // Add global variables here
        APP_ENV = "dev"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                checkout scm   // Works automatically in multibranch pipelines
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing dependencies..."
                sh 'npm install'   // replace with mvn install / pip install etc.
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
                sh 'npm run build'  // replace with your build command
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                sh 'npm test'       // replace with mvn test / pytest etc.
            }
        }

        stage('Package Artifact') {
            steps {
                echo "Packaging artifacts..."
                sh 'zip -r build.zip build/'  // Example package step
                archiveArtifacts artifacts: 'build.zip'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'   // Only deploy when building main branch
            }
            steps {
                echo "Deploying to environment: ${APP_ENV}"
                sh 'echo "Deploying application..."'
                // insert kubectl, ansible, terraform, scp etc.
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
