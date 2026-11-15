pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        IMAGE      = 'flask-web'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
    }

    stages {
        stage('Checkout from Git') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --build-arg BUILD_NUMBER=${BUILD_NUMBER} -t ${IMAGE}:${BUILD_NUMBER} .'
            }
        }

        stage('Load Image into Kubernetes') {
            steps {
                sh '''
                    docker save -o image.tar ${IMAGE}:${BUILD_NUMBER}
                    sudo /usr/local/bin/k3s ctr -n k8s.io images import image.tar
                    rm -f image.tar
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s/IMAGE_TAG/${BUILD_NUMBER}/" k8s/app.yaml | kubectl apply -f -
                    kubectl rollout status deployment/flask-web --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -o wide
                    kubectl get svc flask-web-service
                    IP=$(curl -s http://checkip.amazonaws.com)
                    echo "=========================================="
                    echo " DEPLOYED BUILD ${BUILD_NUMBER} TO KUBERNETES"
                    echo " Website : http://$IP:30080"
                    echo "=========================================="
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline finished: new version is live on Kubernetes.' }
        failure { echo 'Pipeline failed: read the red stage above for the error.' }
        always  { sh 'docker image prune -f || true' }
    }
}
