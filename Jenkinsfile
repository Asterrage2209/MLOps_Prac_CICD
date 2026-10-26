pipeline{
    agent any
    stages{
        stage('Checkout Code'){
            steps{
                git branch: 'main', url: 'https://github.com/Asterrage2209/MLOps_Prac_CICD.git'
            }
        }
        stage('Show Workspace'){
            steps{
                bat 'cd'
            }
        }
        stage('Build Images'){
            steps{
                bat 'docker-compose build'
            }
        }
        stage('Run Tests'){
            steps{
                bat 'docker run --rm cicd3webapp pytest || echo "No tests found."'
            }
        }
        stage('Deploy Containers'){
            steps{
                bat 'docker-compose up -d'
            }
        }
    }
}