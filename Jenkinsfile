pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask_app_personal'
        AWS_EC2_IP = '44.211.168.69'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', credentialsId: 'git', url: 'https://github.com/orikerbis/personal_project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${BUILD_ID}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python -m unittest discover -s tests'
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-token') {
                        dockerImage.push("${BUILD_ID}")
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['aws']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@${AWS_EC2_IP} \
                    'docker login -u orikerbis -p docker-hub-token && \
                    docker pull orikerbis/${DOCKER_IMAGE}:${BUILD_ID} && \
                    docker run -d -p 80:5000 orikerbis/${DOCKER_IMAGE}:${BUILD_ID}'
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
