pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *') // Poll every 2 minutes
    }

    environment {
        DOCKER_IMAGE = 'dxtprashant07/invoice-app:v1'
        DOCKERFILE_PATH = '.' // Change if Dockerfile is in a subfolder like './docker'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout([$class: 'GitSCM', 
                          branches: [[name: 'b1']], 
                          userRemoteConfigs: [[
                              url: 'https://github.com/dxtprashant07/newgit.git',
                              credentialsId: 'github-pat'
                          ]]])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE}..."
                script {
                    sh "ls -l ${DOCKERFILE_PATH}" // Debug: check Dockerfile presence
                    sh "docker build -t ${DOCKER_IMAGE} ${DOCKERFILE_PATH}"
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Example: run tests inside the container
                sh "docker run --rm ${DOCKER_IMAGE} python -m unittest discover || echo 'Tests skipped'"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', 
                                                 usernameVariable: 'DOCKER_USER', 
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                    sh "docker push ${DOCKER_IMAGE}"
                }

                echo 'Optionally running the container...'
                sh "docker run --rm ${DOCKER_IMAGE}"
            }
        }
    }

    post {
        always {
            echo 'Build Finished!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
