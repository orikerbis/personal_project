pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'flaskapp_personal', description: 'Docker image name')
        string(name: 'DOCKERHUB_USERNAME', defaultValue: 'orikerbis', description: 'Docker Hub username')
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to build')
        string(name: 'AWS_EC2_IP', defaultValue: '34.239.114.212', description: 'EC2 instance IP address')
    }

    environment {
        BUILD_ID = "${env.BUILD_ID}"  // Use Jenkins build ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: "${params.BRANCH_NAME}", credentialsId: 'git', url: 'https://github.com/orikerbis/personal_project.git'
            }
        }

        stage('Set Up Docker Buildx') {
            steps {
                sh '''
                docker buildx create --use || true
                docker buildx inspect --bootstrap || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${params.DOCKER_IMAGE}:${BUILD_ID}")
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

        stage('Tag Docker Image') {
            steps {
                script {
                    sh "docker tag ${params.DOCKER_IMAGE}:${BUILD_ID} ${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID}"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-token') {
                        sh "docker push ${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID}"
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                // Debugging Step: Print the IP to ensure it's correctly passed
                echo "Deploying to EC2 instance at ${params.AWS_EC2_IP}"

                sshagent (credentials: ['aws']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@${params.AWS_EC2_IP} << EOF
                    # Stop any existing containers using port 80
                    docker ps --filter "publish=80" -q | xargs --no-run-if-empty docker stop

                    # Remove containers that are stopped and using the same image
                    if [ \$(docker ps -a -q --filter ancestor=${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID}) ]; then
                      docker rm \$(docker ps -a -q --filter ancestor=${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID})
                    fi

                    # Pull the latest image and run the new container
                    docker pull ${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID}
                    docker run -d --platform linux/amd64 -p 80:5000 ${params.DOCKERHUB_USERNAME}/${params.DOCKER_IMAGE}:${BUILD_ID}
                    EOF
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
