def worker = "jenkins_changelog"

pipeline {
  agent none
  environment {
    CL_DIR = "changelogs.${BUILD_NUMBER}"
  }
  options {
    timestamps()
    skipDefaultCheckout true
  }

  stages {
    stage('Stashing Changelogs') {
      agent { label 'master' }
      steps {
        checkout scm
        sh "${WORKSPACE}/jenkins_changelog/stash_changes.sh"
        stash includes: "${CL_DIR}/*", name: 'ChangeLogs'
      }
    }

    stage('Processing Changelogs') {
      agent { label "${worker}" }
      steps {
        unstash 'ChangeLogs'
        checkout scm
        sh "${WORKSPACE}/jenkins_changelog/process_changes.sh"
      }
      post {
        always {
          archiveArtifacts artifacts: 'since_*.html', fingerprint: true
        }
      }
    }
  }
}
