```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat 'if exist .venv rmdir /s /q .venv'
                bat 'python -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Verify Pytest') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest --version'
            }
        }

        stage('Run Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: NotesApp tests passed.'
        }

        failure {
            echo 'FAILURE: Check Console Output.'
        }

        always {
            echo 'NotesApp pipeline completed.'
        }
    }
}
```
