pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Aryyaman/class-management-system.git'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t cms .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop cms || true
                docker rm cms || true
                docker run -d -p 5000:5000 --name cms cms
                '''
            }
        }

    }
}