pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Aryyaman/class-management-system.git'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'sudo docker build -t cms .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                sudo docker stop cms || true
                sudo docker rm cms || true
                sudo docker run -d -p 5000:5000 --name cms cms
                '''
            }
        }

    }
}