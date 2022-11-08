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
        // SNAP_VERSION = ''
    }
    stages {        
        stage ('checkout'){
            steps{
                script{
                    deleteDir()
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], \
                    extensions: [], userRemoteConfigs: [[credentialsId: 'gitlab-jenkins-8-11', url: 'git@gitlab.com:liz.asraf/portfolio-app.git']]])
                    sh 'git fetch --all --tags'
                } 
            }
        }

        stage ('build and unit-test') {           
            steps {
                script{
                    sh """
                        docker build --tag blogapp:latest --file Dockerfile .
                        docker build --tag nginx-new:latest --file Dockerfile-nginx .
                        docker compose up -d
                    """
                    timeout(1) {
                        sh "bash unit-test.sh" 
                    }
                        
                }
            }
        }

        stage ('e2e test') {
            when {anyOf{
                    branch "main" ; branch pattern: "feature/.*", comparator: "REGEXP"
                }
            }            
            steps {
                script{
                    timeout(5) {
                        sh "bash e2e-test.sh"
                    }                                   
                }
            }
        }


        stage ('calculate tag') {
            when {
                branch "main"
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
                    sh "git tag -a v${newtag} -m 'my new version ${newtag}'"
                        sh "git push --tag"
                }
            }
        }

        // stage ('publish') {
        //     when {anyOf{
        //             branch "main" ; branch pattern: "feature/.*", comparator: "REGEXP"
        //         }
        //     }
        //     steps {
        //         script{

        //             echo "login into ecr"
        //             sh "aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com"
        //             if ( BRANCH_NAME != "main" ){ 
        //                 echo "taggging image"
        //                 sh "docker tag app:1.1-SNAPSHOT 644435390668.dkr.ecr.us-west-2.amazonaws.com\\/tedsearch-liz:${RELEASE_VERSION}"
        //                 echo "pushing"
        //                 sh "docker push 644435390668.dkr.ecr.us-west-2.amazonaws.com/tedsearch-liz:${RELEASE_VERSION}"
        //                 sh "git tag -a v${RELEASE_VERSION} -m 'my new version ${RELEASE_VERSION}'"
        //                 withCredentials([gitUsernamePassword(credentialsId: 'ba51f8cb-c38f-46a1-bdbe-333379662541')]) {
        //                     sh "git push --tag"
        //                 }
        //                 sh """cd app
        //                     sed -i 's/image: app:1.1-SNAPSHOT/image: 644435390668.dkr.ecr.us-west-2.amazonaws.com\\/tedsearch-liz:${RELEASE_VERSION}/g' docker-compose.yml"""           
        //             }
        //             else{
        //                 echo "taggging image"
        //                 sh "docker tag app:1.1-SNAPSHOT 644435390668.dkr.ecr.us-west-2.amazonaws.com\\/tedsearch-liz:${RELEASE_VERSION}-test"
        //                 echo "pushing"
        //                 sh "docker push 644435390668.dkr.ecr.us-west-2.amazonaws.com/tedsearch-liz:${RELEASE_VERSION}-test"
        //                 sh """cd app
        //                     sed -i 's/image: app:1.1-SNAPSHOT/image: 644435390668.dkr.ecr.us-west-2.amazonaws.com\\/tedsearch-liz:${RELEASE_VERSION}-test/g' docker-compose.yml"""           
        //             }
        //         }
        //     }
        // }
        
        // stage ('e2e tests'){            
        //     steps {
        //         script{
        //             if ( NEED_E2E_TESTS == "yes" ){
        //                 env.START_DATE = sh (script: "echo \$(date +%s)", returnStdout: true).trim()
        //                 print env.START_DATE
        //                 sh "terraform init"    
        //                 if ( BRANCH_NAME != "main" ){ 
        //                     sh "terraform workspace new test-${START_DATE}"
        //                     sh 'terraform apply -auto-approve'
        //                 }
        //                 else{
        //                     sh "terraform workspace new maintest-${START_DATE}"
        //                     sh 'terraform apply -auto-approve'
        //                 }
        //                 instance_ip = sh (script: """terraform output instance_public_ip | sed 's/\\[//g' | sed 's/\\(],\\)//g' | sed 's/\\]//g' | sed 's/\\"//g'""", returnStdout: true).trim()
        //                 // echo instance_ip
        //                 count = sh (script: """echo "${instance_ip}" | grep -c ',' """, returnStdout: true).trim()
        //                 countint = count.toInteger()
        //                 i = 1
        //                 while ( i <= countint){
        //                     ip = sh(script: """echo "${instance_ip}" | head -n \$((3+$i)) | tail -n 1 | cut -d ',' -f1 """, returnStdout: true).trim()
        //                     echo ip
        //                     sh "zip all_data.zip app/docker-compose.yml app/.env e2e_test.sh app/default.conf -r app/src/main/resources script.sh"
        //                     sh """scp -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" all_data.zip  ubuntu@$ip:/home/ubuntu"""
        //                     sh """ssh -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" ubuntu@$ip "sudo apt install zip -y; unzip all_data.zip; ./script.sh;" """ 
        //                     sh """ssh -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" ubuntu@$ip "aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com; docker compose -f app/docker-compose.yml up -d;" """
        //                     timeout(1) {
        //                     sh """ssh -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" ubuntu@$ip ./e2e_test.sh""" 
        //                     }
        //                     i++
        //                 }
        //                 if ( BRANCH_NAME == "main" ){ 
        //                     sh """sed -i 's/enviroment = "Dev"/enviroment = "Prod"/g' terraform.tfvars"""
        //                     sh "aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com"                            
        //                     echo "taggging image"
        //                     sh "docker tag app:1.1-SNAPSHOT 644435390668.dkr.ecr.us-west-2.amazonaws.com\\/tedsearch-liz:latest"
        //                     echo "pushing"
        //                     sh "docker push 644435390668.dkr.ecr.us-west-2.amazonaws.com/tedsearch-liz:latest"                  
        //                     sh "terraform workspace select production"
        //                     instance_ip = sh (script: """terraform output instance_public_ip | sed 's/\\[//g' | sed 's/\\(],\\)//g' | sed 's/\\]//g' | sed 's/\\"//g'""", returnStdout: true).trim()
        //                     count = sh (script: """echo "${instance_ip}" | grep -c ',' """, returnStdout: true).trim()
        //                     countint = count.toInteger()
        //                     i = 1
        //                     ip = sh(script: """echo "${instance_ip}" | head -n \$((3+$i)) | tail -n 1 | cut -d ',' -f1 """, returnStdout: true).trim()
        //                     echo ip
        //                     sh """ssh -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" ubuntu@$ip "docker compose -f app/docker-compose.yml down" """ 
        //                     sh """ssh -o StrictHostKeyChecking=no -i "~/.aws/lizasraf.pem" ubuntu@$ip "aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-west-2.amazonaws.com; docker pull 644435390668.dkr.ecr.us-east-1.amazonaws.com/tedsearch-liz:latest; docker compose -f app/docker-compose.yml up -d;" """                       
        //                 }
        //             }
        //         }            
        //     }
        // }
    }
    post {
        always {
            script{
                // if ( BRANCH_NAME == "main" ){ 
                // sh "terraform workspace select maintest-${START_DATE}"
                // sh 'terraform destroy -auto-approve'
                // sh "terraform workspace select default"
                // sh "terraform workspace delete maintest-${START_DATE}"
                // }
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
                // if ( env.BRANCH_NAME == 'feature/.*'  ){
                //     emailext body: 'bla bla bla', subject: 'publish failure', to: 'liz161@gmail.com'
                // }
                // else{ 
                    echo "1..2.3 failure"
                // }
            }
        }
    }   
}
                    ////////////////////////////////////list of running ec2's with liz's tags
                    // aws ec2 describe-instances --filters Name=tag:createdby,Values=liz.asraf Name=instance-state-name,Values=running --query "Reservations[].Instances[].InstanceId"                     // }