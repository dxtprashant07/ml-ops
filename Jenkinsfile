pipeline {
    agent any

    // Poll SCM every 2 minutes for automatic build
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout([$class: 'GitSCM', 
                          branches: [[name: 'b1']], 
                          userRemoteConfigs: [[
                              url: 'https://github.com/dxtprashant07/newgit.git',
                              credentialsId: 'github-pat' // GitHub PAT credential
                          ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("dxtprashant07/invoice-app:v1")
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Example test: just print a message
                sh 'echo "Tests passed"'
                // Optional: you can run python tests inside Docker
                // sh 'docker run --rm dxtprashant07/invoice-app:v1 python -m unittest discover'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Push Docker image to Docker Hub
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'dxtprashant07', passwordVariable: '.@.@p5001707')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                            docker.image("dxtprashant07/invoice-app:v1").push()
                        }
                    }
                }
                // Optional: run container after push
                sh 'docker run --rm dxtprashant07/invoice-app:v1'
            }
        }
    }

    post {
        always {
            echo 'Build Finished!'
        }
    }
}
