pipeline {
    agent any

    // Poll SCM every 2 minutes for automatic build
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from b1 branch...'
                checkout([$class: 'GitSCM', 
                          branches: [[name: 'b1']], 
                          userRemoteConfigs: [[
                              url: 'https://github.com/dxtprashant07/ml-ops.git',
                              credentialsId: 'github-pat' // Make sure this credential exists in Jenkins
                          ]]
                ])
            }
        }

        stage('Debug Workspace') {
            steps {
                echo 'Listing workspace contents...'
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image dxtprashant07/invoice-app:v1...'
                script {
                    // Build Docker image using Dockerfile in the root
                    docker.build("dxtprashant07/invoice-app:v1")
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests inside Docker container...'
                // Example: run a simple command inside the container
                sh 'docker run --rm dxtprashant07/invoice-app:v1 echo "Tests passed"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                            docker.image("dxtprashant07/invoice-app:v1").push()
                        }
                    }
                }
                echo 'Running the Docker container...'
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
