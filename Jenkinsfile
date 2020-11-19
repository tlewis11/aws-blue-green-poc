node {
  properties(
    [
        parameters(
            [password(name: 'AWS_ACCESS_KEY_ID'),
             password(name: 'AWS_SECRET_ACCESS_KEY')]
            )

    ])
    stage('Checkout Github Repo') {
      checkout scm
    }

    stage('Deploy Cloudformation Stack') {
      environment {
        AWS_ACCESS_KEY_ID = params.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = params.AWS_SECRET_ACCESS_KEY
      }
      sh 'pip3.8 install -r requirements.txt'
      sh 'python3.8 cloudformation_factory.py'
    }
}
