pipeline {
   agent any
   stages {
      stage('Build front angular'){
         steps {
            echo 'Building front angular app'
            dir ('front/'){
               sh 'npm install'
               sh 'npm run build'
            }
         }
      }
      stage('Docker up') {
         steps {
            echo 'Running on Docker'
            dir ('./'){
               sh 'docker network disconnect gestion-visitantes_default mysql'
               sh 'docker-compose down --rmi all'
               sh 'docker-compose up -d'
               sh 'docker network ls'
               sh 'docker network connect gestion-visitantes_default mysql'
            }
         }
      }
   }
   post { 
      always { 
         deleteDir()
      }
      success {
         echo 'I succeeeded!'
      }
      unstable {
         sh 'docker-compose down'
         echo 'I am unstable :/'
      }
      failure {
         sh 'docker-compose down'
         echo 'I failed :('
      }
      changed {
         echo 'Things were different before...'
      }
   }
}