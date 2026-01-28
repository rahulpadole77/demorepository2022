
pipeline {
    agent any   // Use any available Jenkins agent/runner

    parameters {
    choice(name: 'ENV', choices: ['dev', 'qa', 'prod'], description: 'Target environment')
    booleanParam(name: 'AUTO_APPROVE', defaultValue: false, description: 'Skip approvals (use with caution)')
    }
  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '30'))
    disableConcurrentBuilds() // avoid two deployments racing
  }
    
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
        DL_SUCCESS = 'rahul.padole@gmail.com'
        CHANGE_ID =12234

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
                        python ${SCRIPT_TO_RUN}
                    '''
             }
        }

          
        stage('Install Dependencies') {
            steps {                  
                echo "Installing dependencies..."
                bat 'mvn -B clean install'   // replace with mvn install / pip install etc.                    
            }
        }

       stage('Approval Gate (dev/Main only)') {
          when {
            allOf {
              expression { params.ENV == 'dev' }
              branch 'main'
              expression { !params.AUTO_APPROVE }
            }
          }
          steps {
            script {
              def approver = emailAndWaitForApproval(
                recipients: 'rahul.padole@gmail.com,reyansh.rahul.2025@gmail.com',
                title: "Approve DEV deployment for ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                timeoutMins: 60,
                submitter: 'release.manager,prod.owner,qa.lead',   // users or groups
                params: [
                  'Git Commit' : (env.GIT_COMMIT ?: 'N/A'),
                  'Branch'     : (env.BRANCH_NAME ?: 'N/A'),
                  'Build URL'  : env.BUILD_URL,
                  'Env'        : params.ENV
                ],
                detailsHtml: """
                  <p>This will deploy the following build to <b>PROD</b>.</p>
                  <ul>
                    <li>Artifact: <code>app-1.0.0.jar</code> (example)</li>
                    <li>Change Ticket: <code>${CHANGE_ID ?: 'N/A'}</code></li>
                  </ul>
                """
              )
              if (!approver) {
                currentBuild.result = 'ABORTED'
                error('Approval timed out or approver identity not captured.')
              } else {
                echo "Approved by: ${approver}"
              }
            }
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
            
            emailext(
                    subject: "[SUCCESS] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    to: "${DL_SUCCESS}",
                    mimeType: 'text/html',
                    body: """
                      <h3>Build Succeeded</h3>
                      <p><b>Job:</b> ${env.JOB_NAME} #${env.BUILD_NUMBER}</p>
                      <p><b>Branch:</b> ${env.BRANCH_NAME ?: 'N/A'}</p>
                      <p>${env.BUILD_URL}Open Build</a> |
                         ${env.BUILD_URL}consoleConsole</a></p>
                    """,
                    attachLog: true,
                    compressLog: true,
                    attachmentsPattern: 'report.txt'
                  )

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
