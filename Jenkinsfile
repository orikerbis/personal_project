pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask_app_personal'
        AWS_EC2_IP = '54.87.208.131'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', credentialsId: 'git2', url: 'https://github.com/orikerbis/personal_project.git'
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
                    docker.withRegistry('https://index.docker.io/v1/', '983a5012-6bb2-41a5-92ba-1e8ca480391c') {
                        dockerImage.push("${BUILD_ID}")
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@${AWS_EC2_IP} \
                    'docker login -u orikerbis -p dckr_pat_A2Pvefd2JjvtSLA9LcdeklQulWo && \
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
