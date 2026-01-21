
pipeline {
    agent any   // Use any available Jenkins agent/runner
    
    tools {
        maven 'M3'
    }

    environment {
        // Add global variables here
        APP_ENV = "dev"        
        PYTHON = "C:\\Program Files\\Python313\\python.exe"      // Path to Python
        //DEV_SERVER = "dev.example.com"            // Replace with your DEV target
        DEV_DEPLOY_PATH = "C:\\deploy\\app"       // DEPLOY directory in DEV

    }

    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                checkout scm   // Works automatically in multibranch pipelines
            }
        }
        
        stage('Setup Python Environment') {
                    steps {
                        powershell '''
                            Write-Host "Creating virtual environment..."
                            python -m venv venv
                            .\\venv\\Scripts\\activate
                            pip install --upgrade pip                            
                        '''
                    }
       }
          
        stage('Install Dependencies') {
            steps {                  
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
