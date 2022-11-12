pipeline {
    agent any
    tools {
        git 'Default'
    }
    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'All')
    }
    environment {
        RELEASE_VERSION = ''
    }
    stages {        
        stage ('checkout'){
            steps{
                script{
                    deleteDir()
                    checkout([$class: 'GitSCM', branches: [[name: '*/master']], \
                    extensions: [], userRemoteConfigs: [[credentialsId: 'gitlab-jenkins-8-11', url: 'git@gitlab.com:liz.asraf/blogapp_new.git']]])
                    sh 'git fetch --all --tags'
                } 
            }
        }

        stage ('build and unit-test') {           
            steps {
                script{
                    timeout(5) {
                        sh """
                            docker build --tag blogapp:latest --file Dockerfile .
                            docker build --tag nginx-new:latest --file Dockerfile-nginx .
                            docker compose up -d
                        """
                    }
                    timeout(1) {
                        sh "bash unit-test.sh" 
                    }
                        
                }
            }
        }

        stage ('e2e test') {
            when {anyOf{
                    branch "master" ; branch pattern: "feature/.*", comparator: "REGEXP"
                }
            }            
            steps {
                script{
                    timeout(5) {
                        sh "bash e2e-test.sh"
                    }                                   
                    sh "docker compose down"
                }
            }
        }


        stage ('tag and publish') {
            when {
                branch "master"
            }
            steps {
               script{
                    L_TAG = sh (
                        script: "git tag -l  | tail -n 1 | cut -d 'v' -f2",
                        returnStdout: true
                        ).trim()   
                    echo "$L_TAG"
                    if (L_TAG == ''){
                        newtag="1.0.0"
                        echo "the new tag is $newtag" 
                    }
                    else{
                        newtag = sh (script:"bash version_calculator.sh ${L_TAG}", returnStdout: true).trim()
                        echo "the new tag is $newtag"   
                    }
                    echo "login into ecr..."
                    sh "aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com"
                    echo "taggging image"
                    sh "docker tag blogapp:latest 644435390668.dkr.ecr.us-west-2.amazonaws.com/blogapp:${newtag}"
                    echo "pushing..."
                    sh "docker push 644435390668.dkr.ecr.us-west-2.amazonaws.com/blogapp:${newtag}"
                    sh "git tag -a v${newtag} -m 'my new version ${newtag}'"                    
                    sh "git push --tag"
                    RELEASE_VERSION = newtag
                }
            }
        }
// need to change the image name in the app helm charts with the argo cd repository {{with credentials}}
//need also to change the version in the helm chart
        stage ('Deploy') {
            when { branch "master" }
            }
            steps {
                script{
                    checkout([$class: 'GitSCM', branches: [[name: '*/master']], \
                    extensions: [], userRemoteConfigs: [[credentialsId: 'gitlab-jenkins-8-11', url: 'git@gitlab.com:liz.asraf/argo-cd.git']]])                        
                    sh """cd blogapp
                    sed -i 's/version: */version: ${RELEASE_VERSION}/g' Chart.yaml
                    sed -i 's/tag: */tag: "${RELEASE_VERSION}"/g' values.yaml
                    """           
                }
            }
        }
    }
    post {
        always {
            script{
                sh 'git clean -if'
                cleanWs()
            }
        }
        success {
            script{
                echo "success"
            }
        }         
        failure {
            script{
                // emailext body: 'bla bla bla', subject: 'publish failure', to: 'liz161@gmail.com'
                echo "1..2.3 failure"
            }
        }
    }   
}