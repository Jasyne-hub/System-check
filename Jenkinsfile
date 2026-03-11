pipeline {
    agent any {
        stages {
            stage('Hello World'){
                steps{
                    sh 'echo "Hello, DevOps!"'
                }
            }
            stage('Check Environment'){
                steps{
                    sh 'python3 --version'
                }
            }
            stage('System Check'){
                steps{
                    sh 'python3 system_check.py'
                }
            }
        }
    }
}