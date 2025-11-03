pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'b1',
                    url: 'https://github.com/dxtprashant07/invoice-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("dxtprashant07/invoice-app:v1")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                            docker.image("dxtprashant07/invoice-app:v1").push()
                        }
                    }
                }
            }
        }

        stage('Run Container (Optional)') {
            steps {
                script {
                    sh 'docker run --rm dxtprashant07/invoice-app:v1'
                }
            }
        }
    }

    post {
        always {
            echo 'Build Finished!'
        }
    }
}
