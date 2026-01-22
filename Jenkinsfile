
pipeline {
    agent any   // Use any available Jenkins agent/runner
    
    tools {
        maven 'M3'
    }

    environment {
        // Add global variables here
        APP_ENV = "dev"        
        PYTHON_EXE = "C:\\Program Files\\Python313\\python.exe"      // Path to Python
        //DEV_SERVER = "dev.example.com"            // Replace with your DEV target
        DEV_DEPLOY_PATH = "C:\\deploy\\app"       // DEPLOY directory in DEV
        
        REPO_URL       = 'https://github.com/rahulpadole77/demorepository2022.git'
        CREDENTIALS_ID = 'git-access-api'
        VENV_DIR       = 'venv'
        SCRIPT_TO_RUN  = ".\\demo\\src\\main\\resources\\main.py"
        ARTIFACT_DIR   = 'output'


    }

    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                git branch: 'main', 
                    url: "${REPO_URL}",
                    credentialsId:"${CREDENTIALS_ID}"
                //checkout scm   // Works automatically in multibranch pipelines
            }
        }
        
        stage('Setup Python Environment') {
                    steps {
                        powershell '''
                            Write-Host "Creating virtual environment..."
                            python -m venv venv
                            .\\venv\\Scripts\\activate
                            python -m pip install --upgrade pip                           
                        '''
                    }
       }

        
        stage('Run Python Script') {
            steps {
                    powershell '''
                        python -m venv venv
                        .\\venv\\Scripts\\activate
                        ${PYTHON_EXE} ${SCRIPT_TO_RUN}
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
