
pipeline {
    agent any   // Use any available Jenkins agent/runner
    
    tools {
        maven 'M3'
    }

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
                                         
                bat """
                    set JAVA_TOOL_OPTIONS
                    set _JAVA_OPTIONS
                    set MAVEN_OPTS
                    set CLASSPATH
                """
                echo "Installing dependencies..."
                bat 'mvn -B clean install'   // replace with mvn install / pip install etc.
                    
            }
        }
                
        stage('Deploy') {
            when {
                branch 'main'   // Only deploy when building main branch
            }
            steps {
                echo "Deploying to environment: ${APP_ENV}"
                bat 'echo "Deploying application..."'
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
            //cleanWs()
        }
    }
}
