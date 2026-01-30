// --- Helper: send email and wait for approval ---
def emailAndWaitForApproval(Map cfg = [:]) {
  // Required keys with sensible defaults
  def recipients   = cfg.recipients ?: 'reyansh.rahul.2025@gmail.com'
  def title        = cfg.title ?: 'Deployment Approval Required'
  def detailsHtml  = cfg.detailsHtml ?: '<p>Please review and approve.</p>'
  def timeoutMins  = (cfg.timeoutMins ?: 60) as int
  def submitter    = cfg.submitter ?: 'dev_user' // users or groups 'approver.user1,approver.user2'
  def okLabel      = cfg.okLabel ?: 'Approve'
  def paramsToShow = cfg.params ?: [:] // Optional map to display in email

  // Build a simple table for parameters (optional)
  def paramRows = paramsToShow.collect { k, v -> "<tr><td><b>${k}</b></td><td>${v}</td></tr>" }.join('\n')

  // Approval link (works after login)
  def approvalUrl = "${env.BUILD_URL}input/"

  emailext(
    subject: "[ACTION NEEDED] ${title} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    to: recipients,
    mimeType: 'text/html',
    body: """
      <html>
      <body style="font-family:Arial, sans-serif">
        <h2>${title}</h2>
        <p><b>Job:</b> ${env.JOB_NAME} #${env.BUILD_NUMBER}</p>
        <p><b>Branch:</b> ${env.BRANCH_NAME ?: 'N/A'}</p>
        ${detailsHtml}
        {paramRows ? "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;margin-top:8px'>${paramRows}</table>" : ""}
        <p>${env.BUILD_URL}input/<b>Open approval form</b></a> (login required)</p>
        <p style="margin-top:14px">${approvalUrl}<b>Open approval form</b></a> (login required)</p>
        <hr/>
        <p>This link requires Jenkins login. Approval window: ${timeoutMins} minutes.</p>
      </body></html>
    """
  )

  // Wait for approval with timeout & submitter restriction
  def approver = null
  timeout(time: timeoutMins, unit: 'MINUTES') {
    def userInput = input(
      id: 'ApprovalGate',
      message: title,
      ok: okLabel,
      // Users and/or groups allowed to approve (comma-separated).
      // If you specify groups, ensure Role Strategy or Matrix auth maps them correctly.
      submitter: submitter,
      submitterParameter: 'APPROVER',
      parameters: [
        string(name: 'Justification', defaultValue: '', description: 'Reason / Change ticket / CAB ref')
      ]
    )
    //approver = currentBuild.rawBuild.getAction(hudson.model.CauseAction)?.causes?.find { it.userId }?.userId
  }
  return env.APPROVER
}
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
                //bat 'mvn -B clean install'   // replace with mvn install / pip install etc.                    
            }
        }

       stage('Approval Gate (dev)') {
          when {
            allOf {
              //expression { params.ENV == 'dev' }
              //branch 'main'
              expression { !params.AUTO_APPROVE }
            }
          }
          steps {
            script {
              def approver = emailAndWaitForApproval(
                recipients: 'reyansh.rahul.2025@gmail.com',
                title: "Approve DEV deployment for ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                timeoutMins: 60,
                submitter: 'dev_user',   // users or groups
                params: [
                  'Git Commit' : (env.GIT_COMMIT ?: 'N/A'),
                  'Branch'     : env.GIT_BRANCH, //(env.BRANCH_NAME ?: 'N/A')
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
              echo "Approval is given by: ${env.APPROVER}" 
              if (!"${env.APPROVER}") { //approver
                currentBuild.result = 'ABORTED'
                error('Approval timed out or approver identity not captured.')
              } else {
                echo "Approved by the authorized user:${env.APPROVER}" //approver
              }
            }
          }
        }
                
        stage('Deploy') {
          when {           
            anyOf {
                  // Multibranch: regular branch build
                  branch 'main'
                  // Classic Pipeline or values like origin/main
                  expression { env.GIT_BRANCH == 'origin/main' }
                  // PR builds that target main
                  allOf {
                    expression { env.CHANGE_TARGET == 'main' }
                    //changeRequest()  // ensures it's actually a PR context
                    }
                  }
          }

          steps {                
              echo "Deploying to environment: ${APP_ENV}"
              echo "Deploying application..."    

              // --- OR trigger a downstream job (uncomment to use) ---
                 build job: 'TestBuildJan30',
                      parameters: [
                         string(name: 'PARENT_BUILD', value: env.BUILD_TAG),
                         string(name: 'ENV', value: 'dev'),
                         string(name: 'APPROVED_BY', value: params.APPROVED_BY ?: 'dev_user')
                       ],
                       wait: false

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
          emailext(
            subject: "[FAILED] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            to: "${DL_SUCCESS}",
            mimeType: 'text/html',
            body: "<p>See console: ${env.BUILD_URL}consoleConsole Log</a></p>",
            attachLog: true, compressLog: true
          )
      }
        always {
            echo "Cleaning workspace..."
            //cleanWs()
        }
    }
}
