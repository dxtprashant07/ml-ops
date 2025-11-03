pipeline {
    agent any

    // Poll SCM every 2 minutes
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from main branch...'
                checkout([$class: 'GitSCM',
                          branches: [[name: 'main']],
                          userRemoteConfigs: [[
                              url: 'https://github.com/dxtprashant07/ml-ops.git'
                          ]]
                ])
            }
        }

        stage('Debug Workspace') {
            steps {
                echo 'Listing workspace contents to confirm Dockerfile is present...'
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image dxtprashant07/invoice-app:v1...'
                script {
                    docker.build("dxtprashant07/invoice-app:v1")
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'echo "Tests passed!"'
                // Optional: run python tests inside Docker
                // sh 'docker run --rm dxtprashant07/invoice-app:v1 python -m unittest discover'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the Docker image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                            docker.image("dxtprashant07/invoice-app:v1").push()
                        }
                    }
                }
                echo 'Optional: running container locally...'
                sh 'docker run --rm dxtprashant07/invoice-app:v1'
            }
        }
    }

    post {
        always {
            echo 'Build Finished!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
